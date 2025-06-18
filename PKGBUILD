# Maintainer: Your Name <your_email@example.com>
# Replace "Your Name" and "your_email@example.com" with your actual details.

pkgname=hel-blocks
pkgver=0.1.0 # Initial version. Consider updating this for releases or using pkgver() for git versions.
pkgrel=1
pkgdesc="A Tetris-like game with a Helwan Linux theme."
arch=('any') # Python games are architecture-independent
url="https://github.com/helwan-linux/Helwan-Blocks"
license=('MIT') # IMPORTANT: Confirm this license matches your project's license. If not, change it.
depends=('python' 'python-pygame') # Python runtime and Pygame library

# Source from your GitHub repository's main branch
# Using a specific commit hash or a tag is recommended for stable releases.
# For development, you can use #branch=main or a specific commit hash.
source=("git+${url}.git#branch=main")
sha256sums=('SKIP') # Use 'SKIP' because it's a Git source

# pkgver() function for dynamic versioning from Git (uncomment if you want dynamic versioning)
# pkgver() {
#   cd "$srcdir/Helwan-Blocks" # The directory name created by git clone
#   git describe --long --tags | sed 's/\([^-]*-\)g/\1r/;s/\([^-]*\)-\([^-]*\)/\1.\2/'
# }

build() {
  # No specific build steps for a simple Python script
  # The source is already available in "$srcdir/Helwan-Blocks"
  cd "$srcdir/Helwan-Blocks"
}

package() {
  # Create the target directory for the game files
  # This is where the game will be installed on the system
  mkdir -p "$pkgdir/usr/share/$pkgname"

  # Copy the contents of the 'hel-block-game' folder to the installation directory
  # Note: The cloned repo will be in "$srcdir/Helwan-Blocks"
  cp -r "$srcdir/Helwan-Blocks/hel-block-game/"* "$pkgdir/usr/share/$pkgname/"

  # Set executable permissions for the main script
  chmod +x "$pkgdir/usr/share/$pkgname/main.py"

  # Create the target directory for desktop entries
  mkdir -p "$pkgdir/usr/share/applications"

  # Build the .desktop file directly during package()
  # This ensures correct paths by using the pkgname variable
  cat <<EOF > "$pkgdir/usr/share/applications/helwan-blocks.desktop"
[Desktop Entry]
Name=Helwan Blocks
Comment=A Tetris-like game with a Helwan Linux theme.
Exec=python3 /usr/share/${pkgname}/main.py
Icon=/usr/share/${pkgname}/Images/helwan_logo.png
Terminal=false
Type=Application
Categories=Game;ArcadeGame;
EOF

  # Set executable permission for the .desktop file
  chmod +x "$pkgdir/usr/share/applications/helwan-blocks.desktop"
}
