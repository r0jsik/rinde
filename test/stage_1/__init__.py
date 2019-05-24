from rinde.stage import ControllerBase
from rinde.stage.node.input import RadioBox
from rinde.stage.node.pane import Pane
from rinde.stage.node.text import Text
from rinde.stage.node.util import Canvas
from rinde.stage.node.util import Image


class Controller(ControllerBase):
	def __lookup_element(self, node_id, selector):
		return self.nodes[node_id]._debug_lookup_element(selector)
	
	def start(self):
		self.__test_boundary()
		self.__test_password_field()
		self.__test_text_field()
		self.__test_check_box()
		self.__test_radio_box()
		self.__test_pane()
		self.__test_slider()
		self.__test_canvas_view()
		self.__test_image_view()
		self.__test_choice_box()
		self.__test_list_view()
		self.__test_text_area()
		self.__test_text_flow()
	
	def __test_boundary(self):
		boundary_1 = self.nodes["Boundary-1"]
		boundary_2 = self.nodes["Boundary-2"]
		
		assert boundary_1.absolute_position() == (17, 9)
		assert boundary_1.absolute_size() == (49, 54)
		
		assert boundary_2.absolute_position() == (41, 31)
		assert boundary_2.absolute_size() == (4, 4)
	
	def __test_password_field(self):
		assert self.nodes["PasswordField-1"]["text"] == ""
		assert self.nodes["PasswordField-1"]["content-text"] == ""
		
		self.nodes["PasswordField-1"]["text"] = "correct"
		
		assert self.nodes["PasswordField-1"]["text"] == "correct"
		assert self.nodes["PasswordField-1"]["content-text"] == "*******"
	
	def __test_text_field(self):
		assert self.nodes["TextField-1"]["text"] == ""
		assert self.nodes["TextField-1"]["content-text"] == ""
		
		self.nodes["TextField-1"]["text"] = "correct"
		
		assert self.nodes["TextField-1"]["text"] == "correct"
		assert self.nodes["TextField-1"]["content-text"] == "correct"
	
	def __test_check_box(self):
		assert self.nodes["CheckBox"]["selected"] is False
		
		self.nodes["CheckBox"].click()
		
		assert self.nodes["CheckBox"]["selected"] is True
	
	def __test_radio_box(self):
		radio_box_1 = self.nodes["RadioBox-1"]
		radio_box_2 = self.nodes["RadioBox-2"]
		
		assert radio_box_1["selected"] is True
		assert radio_box_2["selected"] is False
		
		radio_box_2.click()
		
		assert radio_box_1["selected"] is False
		assert radio_box_2["selected"] is True
		
		radio_box_3 = RadioBox(self.groups["RadioBox"], "3", selected=True)
		
		assert radio_box_1["selected"] is False
		assert radio_box_2["selected"] is False
		assert radio_box_3["selected"] is True
	
	def __test_pane(self):
		pane = self.nodes["Pane"]
		text = Text()
		subpane = Pane()
		
		pane.insert_node(subpane)
		
		assert text["font-size"] == 0
		assert subpane in pane.children()
		
		subpane.insert_node(text)
		
		assert text["font-size"] != 0
		assert text in subpane.children()
		
		pane.remove_node(subpane)
		
		assert subpane not in pane.children()
	
	def __test_slider(self):
		slider = self.nodes["Slider-1"]
		slider["value"] = 200
		
		assert slider["value"] == 100
		
		slider["value"] = -10
		
		assert slider["value"] == 0
		
		slider["value"] = 200
		
		assert slider["value"] == 100
		
		self.nodes["Slider-3"]["value"] = 200
		self.nodes["Slider-3"]["range"] = 150
	
	def __test_canvas_view(self):
		canvas_view = self.nodes["CanvasView"]
		
		assert canvas_view.absolute_size() == (256, 256)
		
		canvas = Canvas(128, 64)
		canvas_view.set_canvas(canvas)
		canvas.fill(0, 255, 255)
		
		assert canvas_view.absolute_size() == (128, 64)
	
	def __test_image_view(self):
		image_view = self.nodes["ImageView"]
		image = Image("res/test_2.png")
		
		assert image_view.absolute_size() == (128, 128)
		
		image_view.set_image(image)
		
		assert image_view.absolute_size() == (256, 256)
	
	def __test_choice_box(self):
		disposer = self.__lookup_element("ChoiceBox", "disposer")
		
		self.nodes["ChoiceBox"]["placeholder"] = "Select option..."
		
		assert disposer.placeholded_text["text"] == "Option 2"
		
		self.nodes["ChoiceBox"].remove_option("option_2")
		
		assert disposer.placeholded_text["text"] == ""
	
	def __test_list_view(self):
		self.nodes["ListView"].insert_option("Option 0", "option_0", index=0)
		
		assert self.groups["ListView"] == "option_3"
		
		self.nodes["ListView"].remove_option("option_3")
		
		assert self.groups["ListView"].get() is None
		
		self.nodes["ListView"].insert_option("Option 4", "option_4", True, 3)
		
		assert self.groups["ListView"] == "option_4"
	
	def __test_text_area(self):
		self.nodes["TextArea"]["text"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec tempor dapibus condimentum. Donec a malesuada ex, quis posuere nisl. Curabitur a molestie est, a aliquet enim. Integer sit amet nulla in mauris rhoncus tempor id ut tortor."
	
	def __test_text_flow(self):
		self.nodes["TextFlow"]["text"] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\nDonec tempor dapibus condimentum.\nDonec a malesuada ex, quis posuere nisl.\nCurabitur a molestie est, a aliquet enim.\nInteger sit amet nulla in mauris rhoncus tempor id ut tortor.\nUt eu enim id tortor iaculis volutpat.\nMaecenas metus nulla, tristique a leo a, sollicitudin mollis leo.\nMorbi lorem erat, euismod et mauris sed, congue eleifend arcu."
	
	def action_1(self):
		self.nodes["TextField-2"]["text"] = "Very long text typed in the TextField"
	
	def action_2(self):
		self.nodes["RadioBox-1"]["text"] = "Very long description of the RadioBox"
