#!/usr/bin/env python3
"""
Manual Persona Runner - Run all 5 AI personas step-by-step for a Jira ticket

Usage:
    python run_personas_manually.py AEC-456 "Add OAuth 2.0 authentication"
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from personas.requirements_ai import RequirementsAI
from personas.architect_ai import ArchitectAI
from personas.planner_ai import PlannerAI
from personas.developer_ai import DeveloperAI
from personas.unit_test_ai import UnitTestAI

# Load environment variables
load_dotenv()

def print_banner(text):
    """Print a nice banner"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def get_user_approval(stage_name, file_path):
    """Ask user for approval to continue"""
    print(f"\n{'='*70}")
    print(f"🚦 APPROVAL GATE: {stage_name}")
    print(f"📄 Review file: {file_path}")
    print(f"{'='*70}")
    
    while True:
        response = input("\n✅ Approve and continue? (yes/no/edit): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            print("❌ Workflow stopped by user.")
            return False
        elif response in ['edit', 'e']:
            print(f"📝 Please edit the file: {file_path}")
            input("Press Enter when done editing...")
            return True
        else:
            print("Please enter 'yes', 'no', or 'edit'")

def run_manual_workflow(ticket_id, requirements_text):
    """Run all personas manually with approval gates"""
    
    print_banner(f"🚀 Starting Manual Workflow for {ticket_id}")
    
    # Create workflow directory
    workflow_dir = Path(".ai/workflow") / ticket_id
    workflow_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created workflow directory: {workflow_dir}")
    
    # Initialize personas
    print("\n🤖 Initializing AI Personas...")
    try:
        requirements_ai = RequirementsAI()
        architect_ai = ArchitectAI()
        planner_ai = PlannerAI()
        developer_ai = DeveloperAI()
        unit_test_ai = UnitTestAI()
        print("✅ All personas initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing personas: {e}")
        print("💡 Make sure GEMINI_API_KEY is set in your .env file")
        return
    
    # ========== PERSONA 1: Requirements AI ==========
    print_banner("📋 PERSONA 1: Requirements AI")
    print("Analyzing requirements and generating FEATURE_REQUIREMENTS.md...")
    
    try:
        requirements_output = requirements_ai.analyze_requirements(requirements_text)
        req_file = workflow_dir / "FEATURE_REQUIREMENTS.md"
        req_file.write_text(requirements_output)
        print(f"✅ Generated: {req_file}")
        
        if not get_user_approval("Requirements Review", req_file):
            return
            
    except Exception as e:
        print(f"❌ Error in Requirements AI: {e}")
        return
    
    # ========== PERSONA 2: Architect AI ==========
    print_banner("🏗️  PERSONA 2: Architect AI")
    print("Designing system architecture and generating SYSTEM_DESIGN.md...")
    
    try:
        architecture_output = architect_ai.design_architecture(requirements_output)
        arch_file = workflow_dir / "SYSTEM_DESIGN.md"
        arch_file.write_text(architecture_output)
        print(f"✅ Generated: {arch_file}")
        
        if not get_user_approval("Architecture Review", arch_file):
            return
            
    except Exception as e:
        print(f"❌ Error in Architect AI: {e}")
        return
    
    # ========== PERSONA 3: Planner AI ==========
    print_banner("📝 PERSONA 3: Planner AI")
    print("Creating implementation plan and generating IMPLEMENTATION_PLAN.md...")
    
    try:
        plan_output = planner_ai.create_implementation_plan(requirements_output, architecture_output)
        plan_file = workflow_dir / "IMPLEMENTATION_PLAN.md"
        plan_file.write_text(plan_output)
        print(f"✅ Generated: {plan_file}")
        
        # Extract tasks
        tasks = planner_ai.extract_tasks(plan_output)
        print(f"\n📋 Extracted {len(tasks)} tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"   {i}. {task.get('name', 'Unnamed task')}")
        
        if not get_user_approval("Implementation Plan Review", plan_file):
            return
            
    except Exception as e:
        print(f"❌ Error in Planner AI: {e}")
        return
    
    # ========== PERSONA 4: Developer AI ==========
    print_banner("💻 PERSONA 4: Developer AI")
    print("Generating code scaffolding...")
    
    try:
        code_files = developer_ai.generate_code_scaffolding(
            requirements=requirements_output,
            architecture=architecture_output,
            plan=plan_output
        )
        
        print(f"✅ Generated {len(code_files)} code files:")
        for file_path in code_files.keys():
            print(f"   - {file_path}")
        
        # Save generated code
        code_summary_file = workflow_dir / "GENERATED_CODE_SUMMARY.md"
        summary_content = f"# Generated Code Summary\n\n"
        summary_content += f"**Ticket**: {ticket_id}\n"
        summary_content += f"**Files Generated**: {len(code_files)}\n\n"
        summary_content += "## Files\n\n"
        for file_path, content in code_files.items():
            summary_content += f"### {file_path}\n"
            summary_content += f"```\n{content[:200]}...\n```\n\n"
        code_summary_file.write_text(summary_content)
        print(f"📄 Code summary saved to: {code_summary_file}")

        if not get_user_approval("Generated Code Review", code_summary_file):
            return

    except Exception as e:
        print(f"❌ Error in Developer AI: {e}")
        return

    # ========== PERSONA 5: Unit Test AI ==========
    print_banner("🧪 PERSONA 5: Unit Test AI")
    print("Generating unit tests...")

    try:
        test_output = unit_test_ai.generate_unit_tests(
            requirements=requirements_output,
            architecture=architecture_output,
            code_files=code_files
        )

        test_file = workflow_dir / "TEST_SUMMARY.md"
        test_file.write_text(test_output)
        print(f"✅ Generated: {test_file}")

        if not get_user_approval("Unit Tests Review", test_file):
            return

    except Exception as e:
        print(f"❌ Error in Unit Test AI: {e}")
        return

    # ========== COMPLETION ==========
    print_banner("🎉 WORKFLOW COMPLETE!")
    print(f"✅ All personas completed successfully for {ticket_id}")
    print(f"\n📁 Workflow artifacts saved to: {workflow_dir}")
    print("\nGenerated files:")
    print(f"  1. {workflow_dir}/FEATURE_REQUIREMENTS.md")
    print(f"  2. {workflow_dir}/SYSTEM_DESIGN.md")
    print(f"  3. {workflow_dir}/IMPLEMENTATION_PLAN.md")
    print(f"  4. {workflow_dir}/GENERATED_CODE_SUMMARY.md")
    print(f"  5. {workflow_dir}/TEST_SUMMARY.md")
    print("\n💡 Next steps:")
    print("  - Review all generated files")
    print("  - Implement code in demo-app/ or your project")
    print("  - Run tests and validate")
    print("  - Update Jira ticket with workflow link")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_personas_manually.py <TICKET_ID> <REQUIREMENTS>")
        print("\nExample:")
        print('  python run_personas_manually.py AEC-456 "Add OAuth 2.0 authentication with GitHub support"')
        sys.exit(1)

    ticket_id = sys.argv[1]
    requirements = sys.argv[2]

    run_manual_workflow(ticket_id, requirements)

