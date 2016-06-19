# Copyright 2014, Sandia Corporation. Under the terms of Contract
# DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains certain
# rights in this software.

from behave import *

import nose
import numpy
import toyplot.data
import toyplot.testing


@given(u'a sample toyplot.data.Table')
def step_impl(context):
    numpy.random.seed(1324)
    context.data = toyplot.data.Table()
    context.data["foo"] = numpy.arange(0, 144, 15)
    context.data["bar"] = numpy.random.normal(scale=100, size=10)
    context.data["baz"] = numpy.random.choice(["red", "green", "blue"], 10)
    context.data["blah"] = numpy.repeat("", 10)


@given(u'an instance of toyplot.coordinates.Table')
def step_impl(context):
    context.table_axes = context.canvas.table(context.data)


@then(u'the table can be rendered with defaults')
def step_impl(context):
    pass


@then(u'the table can be rendered with header styles')
def step_impl(context):
    context.table_axes.header.column(1).lstyle = {"fill": "red"}


@then(u'the table can be rendered with column styles')
def step_impl(context):
    context.table_axes.column(1).lstyle = {"fill": "red"}


@then(u'the table can be rendered with row styles')
def step_impl(context):
    context.table_axes.row(1).lstyle = {"fill": "green"}


@then(u'the table can be rendered with cell styles')
def step_impl(context):
    context.table_axes.cell(1, 1).lstyle = {"fill": "blue"}


@then(u'the table can be rendered and row styles override column styles')
def step_impl(context):
    context.table_axes.column(1).lstyle = {"fill": "red"}
    context.table_axes.row(1).lstyle = {"fill": "green"}


@then(u'the table can be rendered and cell styles override row styles')
def step_impl(context):
    context.table_axes.row(1).lstyle = {"fill": "green"}
    context.table_axes.cell(1, 1).lstyle = {"fill": "blue"}


@then(u'the table can be rendered and cell styles override column styles')
def step_impl(context):
    context.table_axes.column(1).lstyle = {"fill": "red"}
    context.table_axes.cell(1, 1).lstyle = {"fill": "blue"}


@then(u'the table can be rendered with extra horizontal lines')
def step_impl(context):
    context.table_axes.grid.hlines[0, ...] = "single"


@then(u'the table can be rendered with extra vertical lines')
def step_impl(context):
    context.table_axes.grid.vlines[..., 1] = "single"


@then(u'the table can be rendered with a full grid')
def step_impl(context):
    context.table_axes.grid.hlines[...] = "single"
    context.table_axes.grid.vlines[...] = "single"


@then(u'the table can be rendered with grid styles')
def step_impl(context):
    context.table_axes.grid.style = {"stroke": "lightgray"}
    context.table_axes.grid.hlines[...] = "single"
    context.table_axes.grid.vlines[...] = "single"


@then(u'the table can be rendered with doubled lines')
def step_impl(context):
    context.table_axes.grid.hlines[1, ...] = "double"
    context.table_axes.grid.vlines[..., 1] = "double"


@then(u'the table can be rendered with custom doubled line separation')
def step_impl(context):
    context.table_axes.grid.hlines[1, ...] = "double"
    context.table_axes.grid.vlines[..., 1] = "double"
    context.table_axes.grid.separation = 4


@then(u'the table can be rendered with column offsets')
def step_impl(context):
    context.table_axes.column(0).column_offset = -50
    context.table_axes.column(2).column_offset = 50
    toyplot.log.warning(context.table_axes._cell_column_offset)


@then(u'the table can be rendered with custom header content')
def step_impl(context):
    context.table_axes.header.cell(0, 1).data = "My Column"


@then(u'the table can be rendered with custom cell content')
def step_impl(context):
    context.table_axes.cell(1, 1).data = "My Cell"


@then(u'the table can be rendered with embedded plots')
def step_impl(context):
    numpy.random.seed(1234)
    context.table_axes.body.cell(0, 3).axes().plot(numpy.sin(numpy.linspace(0, 10)))
    context.table_axes.body.cell(1, 3).axes().bars(
        numpy.random.uniform(0.1, 1, size=10))
    context.table_axes.body.cell(2, 3).axes().bars(numpy.random.choice(
        [-1, 1], size=30), color=numpy.random.choice(["red", "blue"], size=30))
    context.table_axes.body.cell(3, 3, rowspan=2).axes().fill(
        3 + numpy.cos(numpy.linspace(0, 5)) + numpy.sin(numpy.linspace(0, 20)))


@then(u'the table can be rendered with custom column widths')
def step_impl(context):
    context.table_axes.column(0).width = 50
    context.table_axes.column(2).width = 250


@then(u'the table can be rendered with left justification')
def step_impl(context):
    context.table_axes.column(0).align = "left"


@then(u'the table can be rendered with center justification')
def step_impl(context):
    context.table_axes.column(2).align = "center"


@then(u'the table can be rendered with right justification')
def step_impl(context):
    context.table_axes.column(2).align = "right"


@then(u'the table can be rendered with a label')
def step_impl(context):
    context.table_axes.label.text = "Quarterly Report"


@then(u'the table can be rendered with multiple embedded axes in merged cells')
def step_impl(context):
    numpy.random.seed(1234)
    context.table_axes.body.column(2).merge().axes().bars(numpy.random.random(20), along="y")
    context.table_axes.body.column(3).merge().axes().bars(numpy.random.random(20), along="y")


@then(u'the table can be rendered with real world units')
def step_impl(context):
    context.table_axes.grid.hlines[...] = "single"
    context.table_axes.grid.vlines[...] = "single"
    context.table_axes.column(0).width = (1, "cm")
    context.table_axes.row(0).height = "1cm"

@then(u'an instance of toyplot.coordinates.Table can be rendered without a header')
def step_impl(context):
    context.canvas = toyplot.Canvas()
    context.table_axes = context.canvas.table(context.data, hrows=0)

@then(u'the table can be rendered using the convenience API')
def step_impl(context):
    context.canvas, context.table_axes = toyplot.table(context.data)


@given(u'a sample toyplot.data.Table containing null values')
def step_impl(context):
    numpy.random.seed(1234)
    context.data = toyplot.data.Table(numpy.random.random((4, 4)))
    for key, column in context.data.items():
        context.data[key] = numpy.ma.masked_where(column < 0.5, column)

@given(u'an instance of toyplot.coordinates.Table with 4 rows and 3 columns')
def step_impl(context):
    context.table_axes = context.canvas.table(rows=4, columns=3)
    context.table_axes.grid.hlines[...] = "single"
    context.table_axes.grid.vlines[...] = "single"

