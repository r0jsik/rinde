from rinde.stage.node import ComplexNode
from rinde.stage.node.region import HybridNode
from rinde.stage.node.text import Text
from rinde.stage.node.util import LayoutComputer
from rinde.property import TupleProperty


class Table(HybridNode):
	def __init__(self, children, **kwargs):
		super(Table, self).__init__(**kwargs)
		
		self.properties.insert("records", TupleProperty(), self.__update_records)
		
		self.__insert_columns(children)
		self.__columns = children
		
		self.set_style_name("table")
	
	def __update_records(self):
		self.__update_columns()
		self.__draw_border()
	
	def __update_columns(self):
		strategy = self.__get_update_column_strategy()
		
		for i, column in enumerate(self.__columns):
			strategy(column, i, column.get_cells())
	
	def __get_update_column_strategy(self):
		records = self["records"]
		column_size = len(self.__columns[0])
		
		if len(records) < column_size:
			return RecordsLessThanCells(records)
		
		elif len(records) > column_size:
			return RecordsMoreThanCells(records)
		
		else:
			return RecordCountSameAsCell(records)
	
	def __draw_border(self):
		position_x = 0
		table_height = self.get_absolute_size("height")
		
		for i, column in enumerate(self.__columns):
			position_y = column["padding"][0]
			column_width = column.get_absolute_size("width")
			
			for j, cell in enumerate(column.children()):
				if j != 0:
					self.background.draw_stroke((position_x, position_y), (position_x + column_width, position_y))
				
				position_y += cell.get_absolute_size("height")
			
			position_x += column_width + 1
			
			if i != len(self.__columns) - 1:
				self.background.draw_stroke((position_x - 1, 0), (position_x - 1, table_height))
	
	def __insert_columns(self, columns):
		for column in columns:
			if isinstance(column, Column):
				self._insert_node(column)
			else:
				raise TypeError("Table's child must be an instance of rinde.stage.node.table.Column")
	
	def update_layout(self):
		position_x = 0
		
		for column in self.__columns:
			column["position-x"] = position_x
			position_x += column.get_absolute_size("width") + 1


class Column(ComplexNode):
	def __init__(self, heading, **kwargs):
		super(Column, self).__init__(**kwargs)
		
		self.__init_head(heading)
		
		self.set_style_name("column")
	
	def __update_head_width(self):
		self.__head.background["size"] = self["width"], self.__head["height"]
	
	def __init_head(self, heading):
		self.__head = Head(heading)
		self._insert_node(self.__head)
	
	def insert_cell(self, text):
		cell = Text(text)
		self._insert_node(cell)
		cell.reset()
	
	def update_layout(self):
		position_y = 0
		
		for cell in self.children():
			cell["position-y"] = position_y
			position_y += cell.get_absolute_size("height")
		
		self.__head.background["size"] = self["size"]
	
	def remove_cell(self, cell):
		self._remove_node(cell)
	
	def get_cells(self):
		return list(self.children())[1:]
	
	def __len__(self):
		return len(self.get_cells())


class Head(HybridNode):
	def __init__(self, text, **kwargs):
		super(Head, self).__init__(**kwargs)
		
		self.__layout_computer = LayoutComputer(self)
		self.__init_text(text)
		
		self.set_style_name("head")
	
	def __init_text(self, text):
		self.__text = Text(text)
		self._insert_node(self.__text)
	
	def update_layout(self):
		self.__layout_computer.center_node_horizontally(self.__text)


class UpdateColumnStartegy(object):
	def __init__(self, records):
		self.records = records
	
	def __call__(self, column, i, cells):
		raise NotImplementedError


class RecordsLessThanCells(UpdateColumnStartegy):
	def __call__(self, column, i, cells):
		for j, cell in enumerate(cells):
			if j < len(self.records):
				cells[j]["text"] = self.records[j][i]
			else:
				column.remove_cell(cells[j])


class RecordsMoreThanCells(UpdateColumnStartegy):
	def __call__(self, column, i, cells):
		for j, record in enumerate(self.records):
			if j < len(column):
				if cells[j]["text"] == record[i]:
					continue
				else:
					cells[j]["text"] = record[i]
			
			column.insert_cell(record[i])


class RecordCountSameAsCell(UpdateColumnStartegy):
	def __call__(self, column, i, cells):
		for j, record in enumerate(self.records):
			cells[j]["text"] = record[i]
