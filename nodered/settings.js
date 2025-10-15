module.exports = {
  flowFile: 'flows.json',
  flowFilePretty: true,
  uiPort: process.env.PORT || 1880,
  diagnostics: { enabled: false },
  editorTheme: {
    projects: { enabled: false }
  },
  functionGlobalContext: {},
  contextStorage: {
    default: { module: 'localfilesystem' }  // persist context for retry queue
  }
}
