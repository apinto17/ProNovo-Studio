import React, { useEffect, useRef } from "react";
import "3dmol";

interface PDBViewerProps {
  pdbData: string | null;
}

export const PDBViewer: React.FC<PDBViewerProps> = ({ pdbData }) => {
  const viewerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!pdbData || !viewerRef.current || !(window as any).$3Dmol) return;

    const $3Dmol = (window as any).$3Dmol;

    const config = { backgroundColor: "white" };
    const viewer = $3Dmol.createViewer(viewerRef.current, config);

    viewer.addModel(pdbData, "pdb");
    viewer.setStyle({}, { cartoon: { color: "spectrum" } });
    viewer.zoomTo();
    viewer.render();
    viewer.zoom(1.2, 1000);
  }, [pdbData]);

  return (
    <div
      ref={viewerRef}
      style={{
        width: "600px",
        height: "600px",
        position: "relative",
      }}
    />
  );
};
