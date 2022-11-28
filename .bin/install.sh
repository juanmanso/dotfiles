git clone --bare git@personal:juanmanso/dotfiles.git $HOME/.cfg
function config {
   /usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME $@
}
mkdir -p .config-backup
config checkout
if [ $? = 0 ]; then
  echo "Checked out config.";
  else
    echo "Backing up pre-existing dot files.";
    config checkout 2>&1 | egrep "\s+\." | awk {'print $1'} | xargs -I{} mv {} .config-backup/{}
fi;
config checkout
config config status.showUntrackedFiles no

# brew install --cask amethyst

## Install VSCode extensions
# code --install-extension anseki.vscode-color
# code --install-extension bierner.color-info
# code --install-extension burkeholland.simple-react-snippets
# code --install-extension dbaeumer.vscode-eslint
# code --install-extension dsznajder.es7-react-js-snippets
# code --install-extension eamodio.gitlens
# code --install-extension EditorConfig.EditorConfig
# code --install-extension esbenp.prettier-vscode
# code --install-extension formulahendry.auto-rename-tag
# code --install-extension GitHub.copilot
# code --install-extension mintlify.document
# code --install-extension ms-azuretools.vscode-docker
# code --install-extension ms-toolsai.jupyter
# code --install-extension ms-toolsai.jupyter-keymap
# code --install-extension ms-toolsai.jupyter-renderers
# code --install-extension ms-toolsai.vscode-jupyter-cell-tags
# code --install-extension ms-toolsai.vscode-jupyter-slideshow
# code --install-extension naumovs.color-highlight
# code --install-extension PKief.material-icon-theme
# code --install-extension quicktype.quicktype
# code --install-extension streetsidesoftware.code-spell-checker
# code --install-extension streetsidesoftware.code-spell-checker-portuguese
# code --install-extension streetsidesoftware.code-spell-checker-spanish
# code --install-extension TabNine.tabnine-vscode
# code --install-extension WallabyJs.quokka-vscode
# code --install-extension wayou.vscode-todo-highlight
