export default {
  py_backend: {
    input: "./schemas/py_openapi.json",
    output: {
      format: "esm",
      mode: "single",
      target: "src/py_api.ts",
      schemas: "src/codegen_models",
      client: "react-query",
      mock: false,
      override: {
        mutator: {
          path: "./custom_instance.ts",
          name: "customInstance",
        },
      },
    },
  },
};
