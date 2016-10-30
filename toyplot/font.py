# Copyright 2014, Sandia Corporation. Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains certain
# rights in this software.

"""Font management and font metrics.
"""

from __future__ import absolute_import

import reportlab.pdfbase.pdfmetrics

import toyplot.units

class Font(object):
    """Base class for objects that can return information about a specific typeface."""
    @property
    def ascent(self):
        """Return the ascent for the given font.

        Returns
        -------
        ascent: number
            ascent of the font in CSS pixels.
        """
        raise NotImplementedError()

    @property
    def descent(self):
        """Return the descent for the given font.

        Returns
        -------
        descent: number
            descent of the font in CSS pixels.
        """
        raise NotImplementedError()

    def width(self, string):
        """Return the width of a string.

        Parameters
        ----------
        string: str
            The text to be measured.

        Returns
        -------
        width: number
            Width of the string in CSS pixels, if rendered using the given font and
            font size.
        """
        raise NotImplementedError()


class Library(object):
    """Base class for objects that can manage information about a collection of fonts."""
    def metrics(style):
        """Lookup a font using CSS style information and return a corresponding Metrics object.

        Parameters
        ----------
        style: dict containing CSS style information

        Returns
        -------
        metrics: instance of :class:`toyplot.font.Metrics`
        """
        raise NotImplementedError()


class ReportlabFont(Font):
    """Use Reportlab to access the metrics for a font.

    Parameters
    ----------
    font_family: str
        PDF font family to use for measurement.
    font_size: number
        Font size for the measurement.  Defaults to CSS pixel units, and
        supports all toyplot :ref:`units`.
    """
    def __init__(self, family, size): # pylint: disable=redefined-outer-name
        self._family = family
        self._size = toyplot.units.convert(size, target="pt", default="px")

    @property
    def ascent(self):
        ascent, descent = reportlab.pdfbase.pdfmetrics.getAscentDescent(self._family, self._size) # pylint: disable=unused-variable
        ascent = toyplot.units.convert(ascent, target="px", default="pt")
        return ascent

    @property
    def descent(self):
        ascent, descent = reportlab.pdfbase.pdfmetrics.getAscentDescent(self._family, self._size) # pylint: disable=unused-variable
        descent = toyplot.units.convert(descent, target="px", default="pt")
        return descent

    def width(self, string):
        width = reportlab.pdfbase.pdfmetrics.stringWidth(string, self._family, self._size)
        width = toyplot.units.convert(width, target="px", default="pt")
        return width

class ReportlabLibrary(Library):
    """Use Reportlab to provide information about standard PDF fonts."""
    def family(self, style):
        """Extract the name of a standard PDF font family from a CSS style dict.

        Parameters
        ----------
        style: dict containing CSS key-value pairs.
        """
        if "font-family" not in style:
            raise ValueError("No font family specified: %s" % style)

        bold = True if style.get("font-weight", "") == "bold" else False
        italic = True if style.get("font-style", "") == "italic" else False
        for font_family in style["font-family"].split(","):
            font_family = font_family.lower()
            if font_family in ReportlabLibrary.family._substitutions:
                font_family = ReportlabLibrary.family._substitutions[font_family]
                return ReportlabLibrary.family._font_table[(font_family, bold, italic)]

        raise ValueError("Unknown font family: %s" % style) # pragma: no cover

    family._font_table = {
        ("courier", False, False): "Courier",
        ("courier", True, False): "Courier-Bold",
        ("courier", False, True): "Courier-Oblique",
        ("courier", True, True): "Courier-BoldOblique",
        ("helvetica", False, False): "Helvetica",
        ("helvetica", True, False): "Helvetica-Bold",
        ("helvetica", False, True): "Helvetica-Oblique",
        ("helvetica", True, True): "Helvetica-BoldOblique",
        ("times", False, False): "Times-Roman",
        ("times", True, False): "Times-Bold",
        ("times", False, True): "Times-Italic",
        ("times", True, True): "Times-BoldItalic",
        }

    family._substitutions = {
        "courier": "courier",
        "helvetica": "helvetica",
        "monospace": "courier",
        "sans-serif": "helvetica",
        "serif": "times",
        "times": "times",
        }

    def font(self, style):
        family = self.family(style)
        return ReportlabFont(family, style["font-size"])
