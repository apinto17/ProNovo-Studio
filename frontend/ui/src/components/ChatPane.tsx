import React, { useState, useRef, useEffect } from "react";
import {
  Box,
  TextField,
  IconButton,
  Paper,
  Typography,
  Stack,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { FileUpload } from "./FileUpload";
import { useMessage, Message } from "sdk";

export const ChatPane = (params: {
  setPdbContent: React.Dispatch<React.SetStateAction<string | null>>;
}) => {
  const { setPdbContent } = params;
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const [fileName, setFileName] = useState<string | null>(null);

  const { sendMessage } = useMessage();

  const handleFileSelect = (file: File) => {
    setFileName(file.name);
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const newMessage: Message = {
      id: messages.length + 1,
      sender: "user",
      content: input,
      data: null,
    };

    let botMessage: Message | null;

    sendMessage({
      message: newMessage,
      onSuccessCallback: (data: Message) => {
        console.log(data);
        botMessage = data;
        if (botMessage.data) {
          setPdbContent(botMessage.data);
        }
        setMessages((prev) => [...prev, newMessage, data]);
      },
    });

    setInput("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    // allows for multi-line edit using shift
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <Paper
      elevation={3}
      sx={{
        height: "90vh",
        display: "flex",
        flexDirection: "column",
        p: 2,
      }}
    >
      {/* Chat messages */}
      <Box
        sx={{
          flexGrow: 1,
          overflowY: "auto",
          p: 1,
          backgroundColor: "#f5f5f5",
          borderRadius: 2,
        }}
      >
        <Stack spacing={1}>
          {messages.map((msg) => (
            <Box
              key={msg.id}
              alignSelf={msg.sender === "user" ? "flex-end" : "flex-start"}
              sx={{
                maxWidth: "75%",
                px: 2,
                py: 1,
                borderRadius: 2,
                bgcolor: msg.sender === "user" ? "primary.main" : "grey.300",
                color: msg.sender === "user" ? "white" : "black",
              }}
            >
              <Typography variant="body1">{msg.content}</Typography>
            </Box>
          ))}
          <div ref={messagesEndRef} />
        </Stack>
      </Box>

      {/* Input box */}
      <Box
        component="form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        sx={{ display: "flex", mt: 2, flexDirection: "row" }}
      >
        <Box
          sx={{
            display: "flex",
            flexDirection: "row",
            width: 1,
          }}
        >
          <div
            style={{
              paddingLeft: "4px",
              paddingRight: "4px",
              alignContent: "center",
            }}
          >
            <FileUpload onFileSelect={handleFileSelect} accept=".ent,.pdb" />
            {fileName && <Typography mt={2}>Selected: {fileName}</Typography>}
          </div>
          <TextField
            fullWidth
            placeholder="Type your message..."
            multiline
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
          />
        </Box>
        <IconButton color="primary" onClick={handleSend} sx={{ ml: 1 }}>
          <SendIcon />
        </IconButton>
      </Box>
    </Paper>
  );
};
