from rinde.stage.node import ComplexNode
from rinde.stage.node.region import ComplexNodeWithBackground
from rinde.stage.node.text import Text
from rinde.property import TupleProperty


class Table(ComplexNodeWithBackground):
	def __init__(self, children, placeholder="", **kwargs):
		super(Table, self).__init__(**kwargs)
		
		self.properties.insert("records", TupleProperty(), self.__update_records)
		
		self.__insert_columns(children)
		self.__columns = children
		
		self.set_style_name("table")
	
	def __update_records(self):
		for i, column in enumerate(self.__columns):
			for record in self["records"]:
				column.insert_cell(record[i])
		
		self.fit_background_size()
	
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
	
	def __init_head(self, heading):
		head = Cell(heading)
		head.set_style_name("head")
		
		self._insert_node(head)
	
	def insert_cell(self, text):
		cell = Cell(text)
		self._insert_node(cell)
		cell.reset()
	
	def update_layout(self):
		position_y = 0
		
		for cell in self.children():
			cell["position-y"] = position_y
			cell.fit_size_in_column(self)
			position_y += cell.get_absolute_size("height") + 1

 
class Cell(ComplexNodeWithBackground):
	def __init__(self, text, **kwargs):
		super(Cell, self).__init__(**kwargs)
		
		self.__init_text(text)
		
		self.set_style_name("cell")
	
	def __init_text(self, text):
		self._insert_node(Text(text))
	
	def fit_size_in_column(self, column):
		self.background["size"] = column.get_absolute_size("width"), self.get_absolute_size("height")
