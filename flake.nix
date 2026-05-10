{
  description = "Lattice - Graph-based markdown/wiki editor built in SETL";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        buildPackages = import ./nix/buildPackages.nix { inherit pkgs; };
        devShell = import ./nix/devShell.nix { inherit pkgs; };
      in
      {
        packages.default = buildPackages.lattice;

        devShells.default = devShell.shell;

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/lattice";
        };
      });
}
