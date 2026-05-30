module.exports = [
  {
    files: ["static/js/**/*.js"],

    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "script"
    },

    rules: {
      semi: ["error", "always"],
      "no-unused-vars": "warn"
    }
  }
];