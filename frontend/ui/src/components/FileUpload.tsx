import React, { useRef } from "react";
import { Input } from "@mui/material";
import UploadFileIcon from "@mui/icons-material/UploadFile";

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  label?: string;
  accept?: string;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  label = "Upload pdb File",
  accept = "*",
}) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div title={label}>
      <UploadFileIcon fontSize="large" color="primary" onClick={handleClick} />
      <Input
        inputRef={fileInputRef}
        type="file"
        onChange={handleChange}
        inputProps={{ accept }}
        sx={{ display: "none" }}
      />
    </div>
  );
};
