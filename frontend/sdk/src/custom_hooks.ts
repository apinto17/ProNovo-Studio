import { Message } from "./codegen_models";
import { useSendMessageMessageSendPost } from "./py_api";

export const useMessage = () => {
  const { mutate } = useSendMessageMessageSendPost();

  const sendMessage = (params: {
    message: Message;
    onSuccessCallback: (response: Message) => void;
  }) => {
    const { message, onSuccessCallback } = params;
    mutate(
      {
        data: message,
      },
      {
        onSuccess: (data: Message) => {
          console.log(data);
          onSuccessCallback(data);
        },
        onError: (error) => {
          console.log(error);
        },
      }
    );
  };

  return { sendMessage };
};
