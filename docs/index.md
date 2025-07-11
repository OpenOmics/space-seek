<div align="center">

  <h1 style="font-size: 250%">space-seek 🔬</h1>

  <b><i>An awesome 10x spatial sequencing pipeline</i></b><br> 
  <a href="https://github.com/OpenOmics/space-seek/actions/workflows/main.yaml">
    <img alt="tests" src="https://github.com/OpenOmics/space-seek/workflows/tests/badge.svg">
  </a>
  <a href="https://github.com/OpenOmics/space-seek/actions/workflows/docs.yml">
    <img alt="docs" src="https://github.com/OpenOmics/space-seek/workflows/docs/badge.svg">
  </a>
  <a href="https://github.com/OpenOmics/space-seek/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/OpenOmics/space-seek?color=brightgreen">
  </a>
  <a href="https://github.com/OpenOmics/space-seek/blob/main/LICENSE">
    <img alt="GitHub license" src="https://img.shields.io/github/license/OpenOmics/space-seek">
  </a>

  <p>
    Spatial-sequencing: The final frontier. These are the voyages of the pipeline, space-seek.<br>It's long term goals: to explore strange new tissues, to seek out new patterns within single-cellular life, to boldly map the transcriptome of cells— one space at a time.
  </p>

</div>  


## Overview

Welcome to space-seek's documentation! This guide is the main source of documentation for users that are getting started with the [long pipeline name](https://github.com/OpenOmics/space-seek/). 

The **`./space-seek`** pipeline is composed several inter-related sub commands to setup and run the pipeline across different systems. Each of the available sub commands perform different functions: 

<section align="center" markdown="1" style="display: flex; flex-wrap: row wrap; justify-content: space-around;">

!!! inline custom-grid-button ""

    [<code style="font-size: 1em;">space-seek <b>run</b></code>](usage/run.md)   
    Run the space-seek pipeline with your input files.

!!! inline custom-grid-button ""

    [<code style="font-size: 1em;">space-seek <b>unlock</b></code>](usage/unlock.md)  
    Unlocks a previous runs output directory.

</section>

<section align="center" markdown="1" style="display: flex; flex-wrap: row wrap; justify-content: space-around;">


!!! inline custom-grid-button ""

    [<code style="font-size: 1em;">space-seek <b>install</b></code>](usage/install.md)  
    Download remote reference files locally.


!!! inline custom-grid-button ""

    [<code style="font-size: 1em;">space-seek <b>cache</b></code>](usage/cache.md)  
    Cache remote software containers locally.  

</section>

**space-seek** is an awesome spatial sequencing pipeline. It relies on technologies like [Singularity<sup>1</sup>](https://singularity.lbl.gov/) to maintain the highest-level of reproducibility. The pipeline consists of a series of data processing and quality-control steps orchestrated by [Snakemake<sup>2</sup>](https://snakemake.readthedocs.io/en/stable/), a flexible and scalable workflow management system, to submit jobs to a cluster.

The pipeline is compatible with data generated from 10x Genomics Visium technologies. As input, it accepts a set of FastQ files and can be run locally on a compute instance or on-premise using a cluster. A user can define the method or mode of execution. The pipeline can submit jobs to a cluster using a job scheduler like SLURM (more coming soon!). A hybrid approach ensures the pipeline is accessible to all users.

Before getting started, we highly recommend reading through the [usage](usage/run.md) section of each available sub command.

For more information about issues or trouble-shooting a problem, please checkout our [FAQ](faq/questions.md) prior to [opening an issue on Github](https://github.com/OpenOmics/space-seek/issues).

## Contribute 

This site is a living document, created for and by members like you. space-seek is maintained by the members of NCBR and is improved by continous feedback! We encourage you to contribute new content and make improvements to existing content via pull request to our [GitHub repository :octicons-heart-fill-24:{ .heart }](https://github.com/OpenOmics/space-seek).

## Citation

If you use this software, please cite it as below:  

=== "BibTex"

    ```
    Citation coming soon!
    ```

=== "APA"

    ```
    Citation coming soon!
    ```

## References

<sup>**1.**  Kurtzer GM, Sochat V, Bauer MW (2017). Singularity: Scientific containers for mobility of compute. PLoS ONE 12(5): e0177459.</sup>  
<sup>**2.**  Koster, J. and S. Rahmann (2018). "Snakemake-a scalable bioinformatics workflow engine." Bioinformatics 34(20): 3600.</sup>  
