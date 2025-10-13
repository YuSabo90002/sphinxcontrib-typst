"""
Typst builder for Sphinx.

This module implements the TypstBuilder class, which is responsible for
building Typst output from Sphinx documentation.
"""

from collections.abc import Iterator
from os import path
from typing import Optional, Set

from docutils import nodes
from sphinx.builders import Builder
from sphinx.util import logging
from sphinx.util.osutil import ensuredir

from sphinxcontrib.typst.pdf import compile_typst_to_pdf
from sphinxcontrib.typst.writer import TypstWriter

logger = logging.getLogger(__name__)


class TypstBuilder(Builder):
    """
    Builder class for Typst output format.

    This builder converts Sphinx documentation to Typst markup files (.typ),
    which can then be compiled to PDF using the Typst compiler.
    """

    name = "typst"
    format = "typst"
    out_suffix = ".typ"
    allow_parallel = True

    def init(self) -> None:
        """
        Initialize the builder.

        This method is called once at the beginning of the build process.
        """
        pass

    def get_outdated_docs(self) -> Iterator[str]:
        """
        Return an iterator of document names that need to be rebuilt.

        For now, we rebuild all documents on every build.

        Returns:
            Iterator of document names that are outdated
        """
        for docname in self.env.found_docs:
            yield docname

    def get_target_uri(self, docname: str, typ: Optional[str] = None) -> str:
        """
        Return the target URI for a document.

        Args:
            docname: Name of the document
            typ: Type of the target (not used for Typst builder)

        Returns:
            Target URI string
        """
        return docname + self.out_suffix

    def prepare_writing(self, docnames: Set[str]) -> None:
        """
        Prepare for writing the documents.

        This method is called before writing begins.
        Writes the template file to the output directory for master documents to import.

        Args:
            docnames: Set of document names to be written
        """
        # Create the writer instance
        self.writer = TypstWriter(self)

        # Write template file for master documents to import
        self._write_template_file()

    def write(
        self,
        build_docnames: Optional[Set[str]],
        updated_docnames: Set[str],
        method: str = "update",
    ) -> None:
        """
        Override write() to preserve toctree nodes.

        By default, Sphinx's Builder.write() calls env.get_and_resolve_doctree()
        which expands toctree nodes into compact_paragraph with links.
        For Typst, we need the original toctree nodes to generate #include() directives.

        This method uses env.get_doctree() instead to preserve toctree nodes.

        Args:
            build_docnames: Document names to build (None = all)
            updated_docnames: Document names that were updated
            method: Build method ('update' or 'all')
        """
        if build_docnames is None or build_docnames == ["__all__"]:
            # build_all
            build_docnames = self.env.found_docs
        if method == "update":
            # build updated and specified
            docnames = set(build_docnames) | set(updated_docnames)
        else:
            # build all
            docnames = set(build_docnames)

        logger.info("preparing documents... ", nonl=True)
        self.prepare_writing(docnames)
        logger.info("done")

        # Write individual documents
        warnings_count = 0
        for docname in sorted(docnames):
            # Use env.get_doctree() instead of env.get_and_resolve_doctree()
            # to preserve toctree nodes (Requirement 13.2)
            doctree = self.env.get_doctree(docname)
            self.env.apply_post_transforms(doctree, docname)

            # Log progress
            logger.info(f"writing output... [{docname}]", nonl=True)

            # Write the document
            self.write_doc(docname, doctree)

            logger.info(" done")

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """
        Write a document.

        This method is called for each document that needs to be written.

        Requirement 13.1: 各 reStructuredText ファイルに対応する独立した
        .typ ファイルを生成する

        Requirement 13.12: ソースディレクトリ構造を保持して出力する

        Args:
            docname: Name of the document
            doctree: Document tree to be written
        """
        # Get the output file path
        destination = path.join(self.outdir, docname + self.out_suffix)

        # Ensure the directory for this specific file exists
        # This handles nested paths like "chapter1/section"
        dest_dir = path.dirname(destination)
        ensuredir(dest_dir)

        # Set current docname for template application logic
        self.current_docname = docname

        # Set the document on the writer
        self.writer.document = doctree

        # Translate the document to Typst markup
        self.writer.translate()

        # Save the output to the file
        with open(destination, "w", encoding="utf-8") as f:
            f.write(self.writer.output)

    def _write_template_file(self) -> None:
        """
        Write the template file to the output directory.

        This writes a separate template.typ file that master documents can import.
        Only writes if a template is configured (not using Typst Universe packages).
        """
        from sphinxcontrib.typst.template_engine import TemplateEngine

        config = self.config

        # Get template configuration
        template_path = getattr(config, "typst_template", None)
        if template_path:
            # Resolve relative path from source directory
            import os

            template_path = os.path.join(self.srcdir, template_path)

        # Skip if using Typst Universe package (no separate template file needed)
        typst_package = getattr(config, "typst_package", None)
        if typst_package:
            return

        # Create template engine
        template_engine = TemplateEngine(
            template_path=template_path,
            search_paths=[self.srcdir],
            parameter_mapping=getattr(config, "typst_template_mapping", None),
            typst_package=typst_package,
            typst_template_function=getattr(config, "typst_template_function", None),
            typst_package_imports=getattr(config, "typst_package_imports", None),
        )

        # Get template content
        template_content = template_engine.get_template_content()

        # Write template file
        template_file_path = path.join(self.outdir, "_template.typ")
        with open(template_file_path, "w", encoding="utf-8") as f:
            f.write(template_content)

        logger.info(f"Template written to {template_file_path}")

    def finish(self) -> None:
        """
        Finish the build process.

        This method is called once after all documents have been written.
        """
        pass


class TypstPDFBuilder(TypstBuilder):
    """
    Builder class for generating PDF output directly from Typst.

    This builder extends TypstBuilder to compile generated .typ files
    to PDF using the typst-py package.

    Requirement 9.3: TypstPDFBuilder extends TypstBuilder
    Requirement 9.4: Generate PDF from Typst markup
    """

    name = "typstpdf"
    format = "pdf"
    out_suffix = ".pdf"

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """
        Write a document as both .typ and .pdf.

        Override to generate .typ file (not .pdf) during the write phase.
        The .pdf will be generated in finish() by compiling the .typ file.

        Args:
            docname: Name of the document
            doctree: Document tree to be written
        """
        # Generate .typ file (not .pdf)
        typ_destination = path.join(self.outdir, docname + ".typ")

        # Ensure the directory exists
        dest_dir = path.dirname(typ_destination)
        ensuredir(dest_dir)

        # Set current docname for template application logic
        self.current_docname = docname

        # Set the document on the writer
        self.writer.document = doctree

        # Translate the document to Typst markup
        self.writer.translate()

        # Save the .typ file
        with open(typ_destination, "w", encoding="utf-8") as f:
            f.write(self.writer.output)

    def finish(self) -> None:
        """
        Finish the build process by compiling Typst files to PDF.

        After the parent TypstBuilder has generated .typ files,
        this method compiles them to PDF using typst-py.

        Only master documents (defined in typst_documents) are compiled to PDF.
        Included documents are not compiled individually.

        Requirement 9.2: Execute Typst compilation within Python
        Requirement 9.4: Generate PDF from Typst markup
        """
        # First, call parent finish() to complete .typ generation
        super().finish()

        # Get master documents from typst_documents config
        typst_documents = getattr(self.config, "typst_documents", [])

        if not typst_documents:
            logger.warning(
                "No documents defined in typst_documents. Nothing to compile."
            )
            return

        logger.info(f"Compiling {len(typst_documents)} master document(s) to PDF...")

        for doc_tuple in typst_documents:
            # doc_tuple format: (sourcename, targetname, title, author)
            docname = doc_tuple[0]
            typ_file = path.join(self.outdir, docname + ".typ")

            if not path.exists(typ_file):
                logger.warning(f"Master document not found: {typ_file}")
                continue

            try:
                # Read Typst content
                with open(typ_file, encoding="utf-8") as f:
                    typst_content = f.read()

                # Compile to PDF
                pdf_bytes = compile_typst_to_pdf(typst_content, root_dir=self.outdir)

                # Write PDF file
                pdf_file = path.join(self.outdir, docname + ".pdf")
                with open(pdf_file, "wb") as f:
                    f.write(pdf_bytes)

                logger.info(f"Generated PDF: {pdf_file}")

            except Exception as e:
                logger.error(f"Failed to compile {typ_file}: {e}")
