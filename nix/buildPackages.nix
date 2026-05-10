{ pkgs }:

let
  setlInterpreter = pkgs.writeShellScriptBin "setl" ''
    echo "$1" | ${pkgs.gawk}/bin/awk '
    {
      gsub(/\{/, " { ")
      gsub(/\}/, " } ")
      gsub(/,/, " , ")
      gsub(/;/, " ; ")
      gsub(/\[/, " [ ")
      gsub(/\]/, " ] ")
      gsub(/\(/, " ( ")
      gsub(/\)/, " ) ")
      print
    }
    ';
  '';

  latticePackage = pkgs.stdenv.mkDerivation {
    name = "lattice";
    version = "1.0.0";

    src = ../.;

    nativeBuildInputs = with pkgs; [
      makeWrapper
      setlInterpreter
    ];

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
    ];

    buildPhase = ''
      mkdir -p $out/bin
      mkdir -p $out/lib/lattice

      cp -r src/setl $out/lib/lattice/
      cp -r src/ui $out/lib/lattice/
      cp -r assets $out/lib/lattice/

      chmod +x $out/lib/lattice/src/ui/gui_bridge
    '';

    installPhase = ''
      makeWrapper \
        $out/lib/lattice/src/ui/gui_bridge \
        $out/bin/lattice \
        --prefix PATH : ${pkgs.lib.makeBinPath (with pkgs; [gawk coreutils findutils gnused gtk3])} \
        --set LATTICE_LIB $out/lib/lattice
    '';

    meta = with pkgs.lib; {
      description = "Graph-based markdown/wiki editor built in SETL";
      license = licenses.mit;
      platforms = platforms.linux ++ platforms.darwin;
    };
  };

in
{
  lattice = latticePackage;
}
