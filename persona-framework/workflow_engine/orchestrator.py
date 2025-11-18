from typing import Dict, Any, Optional, Callable
from pathlib import Path
import json
from datetime import datetime
from google.cloud import firestore, storage
from enum import Enum
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from personas.requirements_ai import RequirementsAI
from personas.architect_ai import ArchitectAI
from personas.planner_ai import PlannerAI
from personas.developer_ai import DeveloperAI
from personas.unit_test_ai import UnitTestAI

class ApprovalStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"

class WorkflowOrchestrator:
    """
    Orchestrates the complete workflow with human approval gates.
    """
    
    def __init__(self, project_id: str, bucket_name: str):
        self.project_id = project_id
        self.bucket_name = bucket_name
        
        # Initialize GCP clients
        try:
            self.db = firestore.Client(project=project_id)
            self.storage_client = storage.Client(project=project_id)
            self.bucket = self.storage_client.bucket(bucket_name)
        except Exception as e:
            print(f"Warning: Could not initialize GCP clients: {e}")
            print("Running in local mode without cloud storage")
            self.db = None
            self.bucket = None
        
        # Initialize AI personas
        self.requirements_ai = RequirementsAI()
        self.architect_ai = ArchitectAI()
        self.planner_ai = PlannerAI()
        self.developer_ai = DeveloperAI()
        self.unit_test_ai = UnitTestAI()
        
    def execute_workflow_with_gates(
        self, 
        ticket_id: str,
        requirements_doc: str,
        context: Optional[Dict[str, Any]] = None,
        approval_callback: Optional[Callable] = None,
        output_dir: str = ".ai/workflow"
    ) -> Dict[str, Any]:
        """
        Execute workflow with human approval gates after each stage.
        
        Args:
            ticket_id: Unique identifier
            requirements_doc: Input requirements
            context: Project context
            approval_callback: Function to call for human approval
            output_dir: Local directory for artifacts
        
        Returns:
            Workflow execution results
        """
        
        print(f"🚀 Starting workflow for {ticket_id} with approval gates")
        
        # Create output directory
        workflow_dir = Path(output_dir) / ticket_id
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        # Create workflow record
        if self.db:
            workflow_ref = self.db.collection('workflows').document(ticket_id)
            workflow_ref.set({
                'ticket_id': ticket_id,
                'status': 'RUNNING',
                'started_at': datetime.utcnow(),
                'current_step': 'requirements_analysis',
                'approval_gates': []
            })
        
        results = {
            'ticket_id': ticket_id,
            'artifacts': {},
            'validation': {},
            'approvals': {},
            'errors': []
        }
        
        try:
            # ========== STAGE 1: Requirements Analysis ==========
            print("\n" + "="*60)
            print("📋 STAGE 1: Requirements Analysis")
            print("="*60)
            
            requirements_output = self.requirements_ai.analyze_requirements(
                requirements_doc, 
                context
            )
            
            req_validation = self.requirements_ai.validate_output(requirements_output)
            results['validation']['requirements'] = req_validation

            if not req_validation['is_valid']:
                print(f"\n❌ Requirements validation failed:")
                print(f"   Validation details: {req_validation}")
                raise ValueError("Requirements validation failed")
            
            req_path = self._save_local_artifact(
                workflow_dir,
                'FEATURE_REQUIREMENTS.md', 
                requirements_output
            )
            results['artifacts']['requirements'] = str(req_path)
            
            # APPROVAL GATE 1
            print(f"\n🚦 APPROVAL GATE 1: Requirements Review")
            print(f"📄 Review document: {req_path}")
            
            approval_1 = self._request_approval(
                None if not self.db else self.db.collection('workflows').document(ticket_id),
                stage="requirements",
                artifact_url=str(req_path),
                callback=approval_callback
            )
            
            results['approvals']['requirements'] = approval_1
            
            if approval_1 != ApprovalStatus.APPROVED:
                print("❌ Requirements not approved. Workflow stopped.")
                return results
            
            print("✅ Requirements approved. Proceeding to architecture...")

            # ========== STAGE 2: Architecture Design ==========
            print("\n" + "="*60)
            print("🏗️  STAGE 2: Architecture Design")
            print("="*60)

            # Retry logic for timeout and overload errors
            max_retries = 3
            import time
            for attempt in range(max_retries):
                try:
                    print(f"   Attempt {attempt + 1}/{max_retries}...")
                    architecture_output = self.architect_ai.design_architecture(
                        requirements_output,
                        context
                    )
                    break  # Success, exit retry loop
                except Exception as e:
                    error_str = str(e).lower()
                    # Check for timeout (504) or overload (503) errors
                    if "timeout" in error_str or "504" in str(e) or "503" in str(e) or "overloaded" in error_str:
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 10  # Exponential backoff: 10s, 20s, 30s
                            print(f"   ⚠️  API error occurred (timeout/overload), waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                            continue
                        else:
                            print(f"   ❌ Failed after {max_retries} attempts")
                            raise
                    else:
                        raise  # Re-raise non-retryable errors

            arch_validation = self.architect_ai.validate_output(architecture_output)
            results['validation']['architecture'] = arch_validation

            if not arch_validation['is_valid']:
                print(f"\n❌ Architecture validation failed:")
                print(f"   Validation details: {arch_validation}")
                raise ValueError("Architecture validation failed")

            arch_path = self._save_local_artifact(
                workflow_dir,
                'SYSTEM_DESIGN.md',
                architecture_output
            )
            results['artifacts']['architecture'] = str(arch_path)

            # APPROVAL GATE 2
            print(f"\n🚦 APPROVAL GATE 2: Architecture Review")
            print(f"📄 Review document: {arch_path}")

            approval_2 = self._request_approval(
                None if not self.db else self.db.collection('workflows').document(ticket_id),
                stage="architecture",
                artifact_url=str(arch_path),
                callback=approval_callback
            )

            results['approvals']['architecture'] = approval_2

            if approval_2 != ApprovalStatus.APPROVED:
                print("❌ Architecture not approved. Workflow stopped.")
                return results

            print("✅ Architecture approved. Proceeding to planning...")

            # ========== STAGE 3: Implementation Planning ==========
            print("\n" + "="*60)
            print("📝 STAGE 3: Implementation Planning")
            print("="*60)

            # Retry logic for timeout and overload errors
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"   Attempt {attempt + 1}/{max_retries}...")
                    plan_output = self.planner_ai.create_implementation_plan(
                        requirements_output,
                        architecture_output,
                        context
                    )
                    break  # Success, exit retry loop
                except Exception as e:
                    error_str = str(e).lower()
                    # Check for timeout (504) or overload (503) errors
                    if "timeout" in error_str or "504" in str(e) or "503" in str(e) or "overloaded" in error_str:
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 10  # Exponential backoff: 10s, 20s, 30s
                            print(f"   ⚠️  API error occurred (timeout/overload), waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                            continue
                        else:
                            print(f"   ❌ Failed after {max_retries} attempts")
                            raise
                    else:
                        raise  # Re-raise non-retryable errors

            plan_path = self._save_local_artifact(
                workflow_dir,
                'IMPLEMENTATION_PLAN.md',
                plan_output
            )
            results['artifacts']['plan'] = str(plan_path)

            tasks = self.planner_ai.extract_tasks(plan_output)
            results['tasks'] = tasks

            # APPROVAL GATE 3
            print(f"\n🚦 APPROVAL GATE 3: Implementation Plan Review")
            print(f"📄 Review document: {plan_path}")
            print(f"📋 Tasks identified: {len(tasks)}")

            approval_3 = self._request_approval(
                None if not self.db else self.db.collection('workflows').document(ticket_id),
                stage="planning",
                artifact_url=str(plan_path),
                callback=approval_callback
            )

            results['approvals']['planning'] = approval_3

            if approval_3 != ApprovalStatus.APPROVED:
                print("❌ Implementation plan not approved. Workflow stopped.")
                return results

            print("✅ Implementation plan approved. Proceeding to code generation...")

            # ========== STAGE 4: Code Generation ==========
            print("\n" + "="*60)
            print("💻 STAGE 4: Code Generation")
            print("="*60)

            generated_files = {}

            for i, task in enumerate(tasks[:3], 1):
                print(f"\n  [{i}/{min(3, len(tasks))}] Generating code for: {task.get('name', 'Unknown task')}")

                # Retry logic for each code generation task
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        if attempt > 0:
                            print(f"     Attempt {attempt + 1}/{max_retries}...")
                        files = self.developer_ai.generate_code(
                            task,
                            architecture_output,
                            context.get('coding_standards') if context else None
                        )
                        generated_files.update(files)
                        break  # Success, exit retry loop
                    except Exception as e:
                        error_str = str(e).lower()
                        if "timeout" in error_str or "504" in str(e) or "503" in str(e) or "overloaded" in error_str:
                            if attempt < max_retries - 1:
                                wait_time = (attempt + 1) * 5  # Shorter backoff: 5s, 10s, 15s
                                print(f"     ⚠️  API error, waiting {wait_time}s before retry...")
                                time.sleep(wait_time)
                                continue
                            else:
                                print(f"     ❌ Failed after {max_retries} attempts")
                                raise
                        else:
                            raise

            if generated_files:
                code_path = self._save_generated_code(workflow_dir, generated_files)
                results['artifacts']['generated_code'] = str(code_path)
                print(f"\n✅ Generated {len(generated_files)} code files")

            # APPROVAL GATE 4
            print(f"\n🚦 APPROVAL GATE 4: Generated Code Review")
            print(f"📄 Review code: {code_path}")
            print(f"📁 Files generated: {len(generated_files)}")

            approval_4 = self._request_approval(
                None if not self.db else self.db.collection('workflows').document(ticket_id),
                stage="code_generation",
                artifact_url=str(code_path),
                callback=approval_callback
            )

            results['approvals']['code_generation'] = approval_4

            if approval_4 != ApprovalStatus.APPROVED:
                print("❌ Generated code not approved. Workflow stopped.")
                return results

            print("✅ Generated code approved. Workflow complete!")

            # ========== STAGE 5: Unit Test Generation (COMMENTED OUT - TO BE ADDED LATER) ==========
            # print("\n" + "="*60)
            # print("🧪 STAGE 5: Unit Test Generation")
            # print("="*60)

            # test_files = self.unit_test_ai.generate_unit_tests(
            #     code_files=generated_files,
            #     architecture=architecture_output,
            #     coding_standards=context.get('coding_standards') if context else None,
            #     test_framework="pytest"
            # )

            # test_summary = self.unit_test_ai.generate_test_summary(test_files)

            # test_path = self._save_test_files(workflow_dir, test_files)
            # test_summary_path = self._save_local_artifact(
            #     workflow_dir,
            #     'TEST_SUMMARY.md',
            #     test_summary
            # )

            # results['artifacts']['unit_tests'] = str(test_path)
            # results['artifacts']['test_summary'] = str(test_summary_path)

            # print(f"\n✅ Generated {len(test_files)} test files")

            # # APPROVAL GATE 5
            # print(f"\n🚦 APPROVAL GATE 5: Unit Tests Review")
            # print(f"📄 Review tests: {test_path}")
            # print(f"📄 Test summary: {test_summary_path}")

            # approval_5 = self._request_approval(
            #     None if not self.db else self.db.collection('workflows').document(ticket_id),
            #     stage="unit_tests",
            #     artifact_url=str(test_summary_path),
            #     callback=approval_callback
            # )

            # results['approvals']['unit_tests'] = approval_5

            # if approval_5 != ApprovalStatus.APPROVED:
            #     print("❌ Unit tests not approved. Workflow stopped.")
            #     return results

            # print("✅ Unit tests approved. Workflow complete!")

            print("\n" + "="*60)
            print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
            print("="*60)

        except Exception as e:
            print(f"\n❌ Workflow failed: {str(e)}")
            results['errors'].append(str(e))
            import traceback
            traceback.print_exc()

        return results

    def _request_approval(
        self,
        workflow_ref,
        stage: str,
        artifact_url: str,
        callback: Optional[Callable] = None
    ) -> ApprovalStatus:
        """Request human approval for a workflow stage."""

        approval_data = {
            'stage': stage,
            'artifact_url': artifact_url,
            'requested_at': datetime.utcnow(),
            'status': ApprovalStatus.PENDING.value
        }

        if workflow_ref:
            workflow_ref.update({
                f'approval_gates.{stage}': approval_data
            })

        # If callback provided, use it
        if callback:
            approval_status = callback(stage, artifact_url)
            if workflow_ref:
                approval_data['status'] = approval_status.value
                approval_data['approved_at'] = datetime.utcnow()
                workflow_ref.update({
                    f'approval_gates.{stage}': approval_data
                })
            return approval_status

        # Manual approval
        print("\n" + "-"*60)
        print(f"APPROVAL REQUIRED: {stage.upper()}")
        print(f"Artifact: {artifact_url}")
        print("-"*60)
        print("\nOptions:")
        print("  1. APPROVED - Proceed to next stage")
        print("  2. REJECTED - Stop workflow")
        print("  3. CHANGES_REQUESTED - Request modifications")

        while True:
            choice = input("\nEnter your choice (1/2/3): ").strip()

            if choice == "1":
                status = ApprovalStatus.APPROVED
                break
            elif choice == "2":
                status = ApprovalStatus.REJECTED
                break
            elif choice == "3":
                status = ApprovalStatus.CHANGES_REQUESTED
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        if workflow_ref:
            approval_data['status'] = status.value
            approval_data['approved_at'] = datetime.utcnow()
            workflow_ref.update({
                f'approval_gates.{stage}': approval_data
            })

        return status

    def _save_local_artifact(self, workflow_dir: Path, filename: str, content: str) -> Path:
        """Save artifact to local filesystem"""
        file_path = workflow_dir / filename
        file_path.write_text(content, encoding='utf-8')
        return file_path

    def _save_generated_code(self, workflow_dir: Path, files: Dict[str, str]) -> Path:
        """Save generated code files"""
        code_bundle = {
            'generated_at': datetime.utcnow().isoformat(),
            'files': files
        }

        file_path = workflow_dir / 'generated_code.json'
        file_path.write_text(json.dumps(code_bundle, indent=2), encoding='utf-8')
        return file_path

    def _save_test_files(self, workflow_dir: Path, test_files: Dict[str, str]) -> Path:
        """Save generated test files"""
        test_bundle = {
            'generated_at': datetime.utcnow().isoformat(),
            'test_files': test_files
        }

        file_path = workflow_dir / 'unit_tests.json'
        file_path.write_text(json.dumps(test_bundle, indent=2), encoding='utf-8')
        return file_path

    def get_workflow_status(self, ticket_id: str) -> Dict[str, Any]:
        """Get current status of a workflow"""
        if not self.db:
            return {'error': 'Database not available'}

        doc = self.db.collection('workflows').document(ticket_id).get()
        if doc.exists:
            return doc.to_dict()
        return {'error': 'Workflow not found'}

