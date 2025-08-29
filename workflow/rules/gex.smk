# Functions and rules for running spaceranger
# to process gene expression assays
# Local imports
from scripts.common import (
    allocated
)


# Data processing spaceranger rules
rule spaceranger_count:
    """
    Data-processing step to processes a single Visium spatial gene expression
    library and produce per-spot gene expression with spatial coordinates. 
    This step performs alignment and quanitification to build a spot-by-gene
    expression matrix, and it also generates an interactive report containing
    important quality-control metrics to evaluate your data.
    @Input:
        None, (scatter-per-sample)
    @Output:
        Web summary interactive HTML report,
        Web summary CSV file,

    """
    output:
        html = join(workpath, "{sample}", "outs", "web_summary.html"),
        csv  = join(workpath, "{sample}", "outs", "metrics_summary.csv"),
    params:
        # Required columns in sample sheet
        sample_name = "{sample}",
        # If id is not provided, it defaults to sample
        sample_id = lambda w: sample_sheet[w.sample]["id"],
        fastqs    = lambda w: sample_sheet[w.sample]["fastqs"],
        cytaimage = lambda w: sample_sheet[w.sample]["cytaimage"],
        slide     = lambda w: sample_sheet[w.sample]["slide"],
        area      = lambda w: sample_sheet[w.sample]["area"],
        # Other options
        # Optionally create BAM files
        create_bam    = lambda _: "true" if create_bams else "false",
        # References files
        transcriptome = refs['gex_transcriptome'],
        # Conditionally provide the probeset
        # based on the reference genome and
        # the assay. Assays that rely on
        # poly-A selection don't have a
        # probeset
        probeset_option = lambda _: "--probe-set={0}".format(refs['probeset'][assay]) \
            if refs['probeset'][assay] else "",
        # Conditional provide a brightfield 
        # microscope image
        bright_image_option = lambda w: "--image={0}".format(sample_sheet[w.sample]['image']) \
            if sample_sheet[w.sample]['image'] else "",
        # Conditional provide a dark background
        # fluorescence microscope image
        dark_image_option = lambda w: "--darkimage={0}".format(sample_sheet[w.sample]['darkimage']) \
            if sample_sheet[w.sample]['darkimage'] else "",
        # Conditional provide a composite colored
        # fluorescence image
        color_image_option = lambda w: "--colorizedimage={0}".format(sample_sheet[w.sample]['colorizedimage']) \
            if sample_sheet[w.sample]['colorizedimage'] else "",
    resources:
        mem    = allocated("mem",  "spaceranger_count", cluster),
        time   = allocated("time", "spaceranger_count", cluster),
        gres   = allocated("gres", "spaceranger_count", cluster),
        tmpdir = tmpdir,
    threads: int(allocated("threads", "spaceranger_count", cluster)),
    container: config["images"]["spaceranger_v4.0.1"],
    shell: """
    # Setups temporary directory for
    # intermediate files with built-in
    # mechanism for deletion on exit
    if [ ! -d "{resources.tmpdir}" ]; then mkdir -p "{resources.tmpdir}"; fi
    tmp=$(mktemp -d -p "{resources.tmpdir}")
    trap 'rm -rf "${{tmp}}"' EXIT
    export TMPDIR="${{tmp}}"

    # Run spaceranger count
    spaceranger count {params.probeset_option} \\
        --sample={params.sample_name} \\
        --fastqs={params.fastqs} \\
        --transcriptome={params.transcriptome} \\
        --cytaimage={params.cytaimage} \\
        --slide={params.slide} {params.bright_image_option} \\
        --area={params.area} {params.dark_image_option} \\
        --create-bam={params.create_bam} {params.color_image_option}
    """
