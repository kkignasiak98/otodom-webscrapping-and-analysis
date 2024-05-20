# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-23.11"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages
  packages = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.poetry
    pkgs.R
    pkgs.apt
    pkgs.gnumake42
    pkgs.bash
    pkgs.libxml2
  ];

  # Sets environment variables in the workspace
  env = {};
  idx = {
    # Search for the extensions you want on https://open-vsx.org/ and use "publisher.id"
    extensions = [
       "ms-toolsai.jupyter"
       "codeium.codeium"
       "ms-python.python"
       "aaron-bond.better-comments"
       "eamodio.gitlens"
       "charliermarsh.ruff"
       "reditorsupport.r"
       "rdebugger.r-debugger"
       "bungcip.better-toml"
       
    ];

    # Enable previews
    previews = {
      enable = true;
      previews = {
      };
    };

    # Workspace lifecycle hooks
    workspace = {
      # Runs when a workspace is first created
      # It might not work if you want to rebuild it along the way.
      onCreate = {
        create_project = "poetry new otodom_analysis";
        create_env = "poetry env use python3.11";
        tool_for_r_update = '' Rscript -e 'install.packages("ropenblas", repos="http://cran.r-project.org")'
        '';
        update_r = '' Rscript -e 'ropenblas::rcompiler("4.3.3")'
        '';
        install_renv = '' Rscript -e 'install.packages("renv", repos="http://cran.r-project.org")'
        '';
        renv_init = '' Rscript -e 'renv::init()'
        '';
        install_r_language_server = '' Rscript -e 'remotes::install_github("REditorSupport/languageserver")'
        '';
      };
      onStart = {
        poetry_sync = "poetry install --sync";
        renv_sync_type = '' Rscript -e 'renv::settings$snapshot.type("all")' 
        ''; # without this settings the renv will only store packages that are installed and used by the project. Check docs: https://rstudio.github.io/renv/articles/faq.html#why-isnt-my-package-being-snapshotted-into-the-lockfile
        renv_sync = '' Rscript -e 'renv::restore()'  
        ''; # it will remove all libraries not listed in renv.lock. Similar to `poetry install --sync`.
      };
    };
  };
}
