{ pkgs }:

let
  setlDevShell = pkgs.mkShell {
    buildInputs = with pkgs; [
      gawk
      coreutils
      findutils
      gnused
      gtk3
      glib
      pango
      gdk-pixbuf
      cairo
      gcc
      pkg-config
    ];

    shellHook = ''
      export LATTICE_DEV=1
      export LATTICE_SRC=$(pwd)/src
      export PATH="$PWD/src/ui:$PATH"

      alias lattice-run="src/ui/gui_bridge"
      alias setl-run="gawk -f src/setl/main.setl"

      echo "Lattice development environment ready"
      echo "SETL source: $LATTICE_SRC"
      echo "Run with: lattice-run"
    '';
  };
in
{
  shell = setlDevShell;
}
