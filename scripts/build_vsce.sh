cd jac/support/vscode_ext/jac
npm install
npm install -g @vscode/vsce
vsce package
# code --install-extension jaclang-*.vsix
cursor --install-extension jaclang-*.vsix
cd -