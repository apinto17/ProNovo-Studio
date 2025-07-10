from typing import List
from langchain.tools import tool
from pydantic import BaseModel
import requests
import os
import json
from agents.schemas import ProteinDesignResult
from langchain.tools import StructuredTool

rf_key = os.getenv("RF_DIFF_KEY")

class ProteinDesignInput(BaseModel):
    input_pdb: str
    hotspot_res: List[str]
    contigs: str
    diffusion_steps: int = 15

def design_protein(input_pdb: str, hotspot_res: list[str], contigs: str, diffusion_steps: int = 15) -> dict:
    
    r = requests.post(
    url=os.getenv("URL", "https://health.api.nvidia.com/v1/biology/ipd/rfdiffusion/generate"),
    headers={"Authorization": f"Bearer {rf_key}"},
    json={
            "input_pdb": input_pdb,
            "contigs": contigs,
            "hotspot_res": hotspot_res,
            "diffusion_steps": diffusion_steps,
        },
    )
    print(r, "Saving to output.pdb:\n", r.text[:200], "...")
    if(r.status_code != 200):
        return ProteinDesignResult(
            message=f"Failed to load due to {r.text}",
            pdb=None
        )
    return ProteinDesignResult(
        message=f"Protein designed with {len(input_pdb)} characters of input and hotspots {hotspot_res} and contigs {contigs}.",
        pdb=json.loads(r.text)["output_pdb"]
    ).model_dump()

rf_diffusion_tool = StructuredTool.from_function(
    func=design_protein,
    name="rf_diffusion_tool",
    description="""Design a protein using RF diffusion. 
    Requires full PDB file content (not just a PDB ID) as input_pdb. 
    Use `pdb_search_tool` first if you need to fetch a PDB file from an ID.

    contigs:

      contigs stands for 'contiguous [protein regions]'. 
      This string defines a protein that is being generated. 
      It is a specification written in a domain-specific language that tells RFdiffusion 
      which part of the input protein are to be kept and what kind of a binder (or a scaffold) needs to be constructed. 
      As an example, a string 'A10-100/0 50-150' instructs RFdiffusion to keep amino acids 10-100 in Chain A [from the input PDB file], 
      then break the chain (special '/0' notation, which signifies the end of the chain and thus effectively 
      makes 'A10-100' a new target protein), and construct a new chain (effectively a binder protein) of length 50 to 150 amino acids.

    hotspot residues:

      The hotspot residues string provides a way to specify which region the new protein (binder) must contact with the original 
      input protein (a target), therefore we can guide a binder to a specific region. These residues must be within the input_pdb
    """,
    args_schema=ProteinDesignInput,
    return_schema=dict,
)

@tool
def pdb_search_tool(pdb_id: str) -> str:
    """Download the full PDB file content from RCSB using the PDB ID (e.g., '1R42')."""
    response = requests.get(f"https://files.rcsb.org/download/{pdb_id}.pdb")
    if response.status_code == 200:
        lines = filter(lambda line: line.startswith("ATOM"), response.text.split("\n"))
        return "\n".join(list(lines)[:100])
    return f"Error fetching {pdb_id}"