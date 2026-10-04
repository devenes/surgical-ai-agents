"""Standalone Multimodal Surgical AI Demonstration Script.

This reference script demonstrates supplemental vision-language understanding
using the official Google GenAI SDK and Vertex AI (`gemini-3.8-flash`).

Architectural Notice:
    This script is strictly independent from the primary text-based
    Coordinator/Specialist multi-agent research workflow.
    It performs neutral visual inspection without patient-specific diagnosis,
    clinical decision support, or surgical guidance.

Usage:
    .venv/bin/python multimodal-demo/adk_multimodal_example.py
    .venv/bin/python multimodal-demo/adk_multimodal_example.py --image path/to/image.png
"""

import argparse
import mimetypes
import os
from pathlib import Path
from typing import Optional

from google import genai
from google.genai import types

# Default project configuration configurable via environment
DEFAULT_PROJECT: Optional[str] = os.environ.get("GOOGLE_CLOUD_PROJECT")
DEFAULT_LOCATION: str = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get(
    "GOOGLE_CLOUD_REGION", "us"
)
DEFAULT_MODEL: str = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")

DEFAULT_IMAGE_PATH = Path(__file__).resolve().parent / "assets" / "laparoscopic_cvs_schematic.png"

DEFAULT_PROMPT = (
    "Describe only the observable visual anatomical and operative features in this image. "
    "Do not diagnose disease, identify a patient, recommend treatment, or infer a clinical decision."
)

FOLLOW_UP_PROMPT = (
    "Based on those observable features, explain what kinds of surgical research or "
    "computer-vision tasks might use similar visual information. Keep the answer educational "
    "and non-clinical."
)


MOCK_STAGE1_OBSERVATION = (
    "The image presents an educational, schematic diagram of the hepatobiliary anatomy relevant to "
    "laparoscopic cholecystectomy and the Critical View of Safety (CVS) as established by Strasberg.\n\n"
    "Visual and Anatomical Features Observed:\n"
    "1. Calot's Triangle (Hepatocystic Triangle): Visible clearance of adipose and fibrous connective tissue "
    "between the liver bed and the gallbladder infundibulum.\n"
    "2. Gallbladder Base / Cystic Plate: Separation of the lower third of the gallbladder from the liver bed, "
    "revealing the cystic plate behind the infundibulum.\n"
    "3. Conduits: Exactly two distinct tubular structures are seen entering the gallbladder directly: "
    "the cystic duct and the cystic artery.\n"
    "4. Surrounding Landmarks: The common hepatic duct and common bile duct are demarcated distally without "
    "unnecessary aggressive dissection.\n\n"
    "Constraint Compliance:\n"
    "- Neutral descriptive appraisal strictly maintained.\n"
    "- No diagnostic claims, patient-specific attributes, or intraoperative cut decisions rendered."
)

MOCK_STAGE2_FOLLOW_UP = (
    "Educational & Computer-Vision Research Applications:\n\n"
    "1. Deep Learning Landmark Detection: Ground-truth annotation datasets (such as EndoVis, Cholec80, and "
    "SafeLap) utilize similar bounding boxes and segmentation masks to evaluate automated anatomical identifier models.\n"
    "2. Automated CVS Verification: Convolutional Neural Networks and Vision Transformers (ViTs) can be trained "
    "to assess Strasberg CVS criteria (calot clearance, cystic plate exposure, two-structure rule) to provide "
    "post-hoc peer review and surgical resident education.\n"
    "3. Spatial Reasoning & Safety Boundaries: Investigating AI failure modes when confronted with severe "
    "inflammation, aberrant anatomy, or surgical clips, highlighting the necessity of human surgeon oversight.\n\n"
    "Constraint Compliance:\n"
    "- Analysis strictly limited to educational research and algorithm benchmarking methodology."
)


def load_image_part(image_path: Path) -> types.Part:
    """Read local image file and wrap as a typed Google GenAI Part."""
    if not image_path.exists():
        raise FileNotFoundError(f"Image asset not found at {image_path}")

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if not mime_type:
        mime_type = "image/png"

    image_bytes = image_path.read_bytes()
    return types.Part.from_bytes(data=image_bytes, mime_type=mime_type)


def execute_multimodal_offline(
    image_path: Path,
    prompt: str,
    model: str = DEFAULT_MODEL,
    run_follow_up: bool = False,
) -> None:
    """Simulate neutral multimodal vision analysis locally with zero network calls and zero tokens."""
    print("=" * 70)
    print("SURGICAL AI MULTIMODAL REFERENCE SCRIPT (ZERO-TOKEN OFFLINE MODE)")
    print("=" * 70)
    print(f"Model:    {model} (Simulated)")
    print("Mode:     Offline Simulation Rehearsal (Conference Resilience)")
    print(f"Image:    {image_path.name} ({image_path.stat().st_size} bytes)")
    print("-" * 70)

    print("\n[Stage 1: Neutral Visual Observation]")
    print(f"Prompt: {prompt}\n")
    print("-" * 70)
    print(MOCK_STAGE1_OBSERVATION)
    print("-" * 70)

    if run_follow_up:
        print("\n[Stage 2: Educational & Research Follow-Up]")
        print(f"Prompt: {FOLLOW_UP_PROMPT}\n")
        print("-" * 70)
        print(MOCK_STAGE2_FOLLOW_UP)
        print("-" * 70)

    print("\n[Safety Notice]")
    print(
        "This demonstration describes visual features for instructional and computer-vision "
        "research appraisal only. It does not provide medical diagnosis, clinical decision "
        "support, or intraoperative operative guidance."
    )
    print("=" * 70)


def execute_multimodal_inquiry(
    image_path: Path,
    prompt: str,
    project: Optional[str] = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
    model: str = DEFAULT_MODEL,
    run_follow_up: bool = False,
    offline: bool = False,
) -> None:
    """Execute live vision-language content generation via Vertex AI or offline simulation."""
    if offline:
        execute_multimodal_offline(
            image_path=image_path,
            prompt=prompt,
            model=model,
            run_follow_up=run_follow_up,
        )
        return

    try:
        print("=" * 70)
        print("SURGICAL AI MULTIMODAL REFERENCE SCRIPT (SUPPLEMENTAL DEMO)")
        print("=" * 70)
        print(f"Model:    {model}")
        print(f"Project:  {project or '(Inferred from ADC)'}")
        print(f"Location: {location}")
        print(f"Image:    {image_path.name} ({image_path.stat().st_size} bytes)")
        print("-" * 70)

        # 1. Load image asset
        image_part = load_image_part(image_path)

        # 2. Initialize Vertex AI client using Application Default Credentials
        client_kwargs = {
            "vertexai": True,
            "location": location,
        }
        if project:
            client_kwargs["project"] = project
        client = genai.Client(**client_kwargs)

        # 3. Configure Gemini 3.8 Flash thinking level
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level="MEDIUM"),
        )

        # 4. Stage 1: Neutral Visual Observation
        print("\n[Stage 1: Neutral Visual Observation]")
        print(f"Prompt: {prompt}\n")

        response = client.models.generate_content(
            model=model,
            contents=[image_part, prompt],
            config=config,
        )

        stage1_text = response.text or "(No text returned)"
        print("-" * 70)
        print(stage1_text)
        print("-" * 70)

        # 5. Optional Stage 2: Educational Research Follow-Up
        if run_follow_up:
            print("\n[Stage 2: Educational & Research Follow-Up]")
            print(f"Prompt: {FOLLOW_UP_PROMPT}\n")

            # Multi-turn conversation payload
            followup_response = client.models.generate_content(
                model=model,
                contents=[
                    image_part,
                    prompt,
                    stage1_text,
                    FOLLOW_UP_PROMPT,
                ],
                config=config,
            )

            stage2_text = followup_response.text or "(No text returned)"
            print("-" * 70)
            print(stage2_text)
            print("-" * 70)

        print("\n[Safety Notice]")
        print(
            "This demonstration describes visual features for instructional and computer-vision "
            "research appraisal only. It does not provide medical diagnosis, clinical decision "
            "support, or intraoperative operative guidance."
        )
        print("=" * 70)
    except Exception as exc:
        print(f"\n[FALLBACK] Live multimodal execution failed ({exc}).")
        print("[FALLBACK] Switching to zero-token offline simulation for presentation resilience...\n")
        execute_multimodal_offline(
            image_path=image_path,
            prompt=prompt,
            model=model,
            run_follow_up=run_follow_up,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run supplemental multimodal vision analysis on surgical imagery."
    )
    parser.add_argument(
        "--image",
        type=Path,
        default=DEFAULT_IMAGE_PATH,
        help="Path to local PNG/JPEG image file.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=DEFAULT_PROMPT,
        help="Instruction prompt constraining the model to neutral visual observation.",
    )
    parser.add_argument(
        "--follow-up",
        action="store_true",
        help="Execute Stage 2 academic informatics follow-up prompt.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Gemini model identifier (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--offline",
        "--mock",
        action="store_true",
        dest="offline",
        help="Run multimodal demonstration in zero-token offline mode (safe for conference presentation).",
    )
    args = parser.parse_args()

    execute_multimodal_inquiry(
        image_path=args.image,
        prompt=args.prompt,
        model=args.model,
        run_follow_up=args.follow_up,
        offline=args.offline,
    )


if __name__ == "__main__":
    main()
