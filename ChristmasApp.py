
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import (ColumnDataSource, ImageURL, Div, Row, Column, 
                          FixedTicker, Select, Slider, TextInput, ColorPicker,
                          Button, FileInput, PreText, Title, CustomJS)
from bokeh.layouts import layout
import pandas as pd
import base64
import io
from bokeh.models import ColumnDataSource, Div, GlobalInlineStyleSheet, InlineStyleSheet

gstyle = GlobalInlineStyleSheet(css=""" html, body, .bk, .bk-root {background-color: #343838; margin: 0; padding: 0; height: 100%; color: white; font-family: 'Consolas', 'Courier New', monospace; } .bk { color: white; } .bk-input, .bk-btn, .bk-select, .bk-slider-title, .bk-headers, .bk-label, .bk-title, .bk-legend, .bk-axis-label { color: white !important; } .bk-input::placeholder { color: #aaaaaa !important; } """)
slider_style = InlineStyleSheet(css=""" /* Host slider container */ :host { background: none !important; } /* Full track: set dark grey, but filled part will override with .noUi-connect */ :host .noUi-base, :host .noUi-target { background: #bfbfbf !important; } /* Highlighted portion of track */ :host .noUi-connect { background: #00ffe0; } /* Slider handle */ :host .noUi-handle { background: #343838; border: 2px solid #00ffe0; border-radius: 50%; width: 20px; height: 20px; } /* Handle hover/focus */ :host .noUi-handle:hover, :host .noUi-handle:focus { border-color: #ff2a68; box-shadow: 0 0 10px #ff2a6890; } /* Tooltip stepping value */ :host .noUi-tooltip { background: #343838; color: #00ffe0; font-family: 'Consolas', monospace; border-radius: 6px; border: 1px solid #00ffe0; } /* Filled (active) slider track */ :host .noUi-connect { background: linear-gradient(90deg, #ffdd30 20%, #fc3737 100%) !important; /* greenish-cyan fade */ box-shadow: 0 0 10px #00ffe099 !important; } """)
textinput_css = InlineStyleSheet(css=""" /* Outer container styling */ :host { background: #181824 !important; border-radius: 14px !important; padding: 16px !important; box-shadow: 0 4px 18px #0006 !important; } /* Title label styling */ :host .bk-input-group label, :host .bk-textinput-title { color: #34ffe0 !important; font-size: 1.14em !important; font-family: 'Fira Code', monospace; font-weight: bold !important; margin-bottom: 12px !important; letter-spacing: 0.5px !important; text-shadow: 0 2px 12px #34ffe077, 0 1px 3px #222; } /* The input box */ :host input[type="text"] { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; padding: 11px 15px !important; font-size: 1.08em !important; transition: border 0.12s, box-shadow 0.12s; box-shadow: none !important; } /* On hover/focus: red border with glowing effect */ :host input[type="text"]:hover, :host input[type="text"]:focus { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 15px #ff3049bb !important; outline: none !important; } /* Placeholder text */ :host input[type="text"]::placeholder { color: #9ca3af !important; opacity: 0.7 !important; font-style: italic !important; } """)
select_css = InlineStyleSheet(css=""" /* Widget container */ :host { background: #181824 !important; border-radius: 14px !important; padding: 16px !important; box-shadow: 0 4px 24px #0007 !important; } /* Title styling */ :host .bk-input-group label, :host .bk-select-title { color: #06f0ff !important; font-size: 1.18em !important; font-family: 'Fira Code', monospace; font-weight: bold !important; margin-bottom: 12px !important; letter-spacing: 1px !important; text-shadow: 0 2px 12px #06f0ff88, 0 1px 6px #111b; } /* Dropdown select */ :host select { background: #23233c !important; color: #f9fafb !important; border: 2px solid #06b6d4 !important; border-radius: 8px !important; padding: 10px 14px !important; font-size: 1.07em !important; transition: border 0.1s, box-shadow 0.1s; box-shadow: none !important; } /* Glow effect on hover/focus */ :host select:hover, :host select:focus { border-color: #ff3049 !important; box-shadow: 0 0 0 2px #ff304999, 0 0 18px #ff3049cc !important; outline: none !important; } """)
base_variables = """ :host { /* CSS Custom Properties for easy theming */ --primary-color: #8b5cf6; --secondary-color: #06b6d4; --background-color: #1f2937; --surface-color: #343838; --text-color: #f9fafb; --accent-color: #f59e0b; --danger-color: #ef4444; --success-color: #10b981; --border-color: #4b5563; --hover-color: #6366f1; background: none !important; } """
file_input_style = InlineStyleSheet(css=base_variables + """ :host input[type="file"] { background: var(--surface-color) !important; color: var(--text-color) !important; border: 2px dashed var(--border-color) !important; border-radius: 6px !important; padding: 20px !important; font-size: 14px !important; cursor: pointer !important; transition: all 0.2s ease !important; } :host input[type="file"]:hover { border-color: var(--primary-color) !important; background: rgba(139, 92, 246, 0.05) !important; } :host input[type="file"]::file-selector-button { background: var(--primary-color) !important; color: white !important; border: none !important; border-radius: 4px !important; padding: 8px 16px !important; margin-right: 12px !important; cursor: pointer !important; font-weight: 600 !important; } """)

BGURLlist = [
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas-background-decoration-with-white-golden-style_497837-359.png",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris1.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris2.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris3.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris4.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris5.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris6.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris7.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris8.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris9.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris10.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris11.jpg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/cris12.jpg"
]

CLURLlist = [
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas_light_bulb_svg%20(1).svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas_light_bulb_svg%20(2).svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas_light_bulb_svg%20(3).svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas_light_bulb_svg%20(4).svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas_light_bulb_svg%20(5).svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas_light_bulb_svg%20(6).svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/christmas_light_bulb_svg%20(7).svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/482277ca3783a230a931d95e8eeb2a6bca6d1400/assets0/christmas_light_bulb_svg.svg",
    "https://raw.githubusercontent.com/mixstam1821/bokeh_showcases/refs/heads/main/assets0/Christmas%20Lights.svg"
]

# Load climate data
try:
    climate_df = pd.read_csv('/home/michael/Desktop/climate_yearly_data.csv')
    climate_data_available = True
except:
    climate_df = None
    climate_data_available = False

years_numeric = climate_df.iloc[:, 0].values
temp_anomaly = climate_df.iloc[:, 1].values

# Global variables to store current data
current_years = years_numeric
current_data = temp_anomaly

curdoc().theme = 'dark_minimal'

def calculate_smooth_rotation_angles(x, y, poly_degree=4, num_points=None):
    if num_points is None:
        num_points = len(x)
    
    coeffs = np.polyfit(x, y, poly_degree)
    poly = np.poly1d(coeffs)
    
    x_dense = np.linspace(x.min(), x.max(), 1000)
    y_dense = poly(x_dense)
    
    dx = np.diff(x_dense)
    dy = np.diff(y_dense)
    segment_lengths = np.sqrt(dx**2 + dy**2)
    cumulative_length = np.concatenate([[0], np.cumsum(segment_lengths)])
    
    target_lengths = np.linspace(0, cumulative_length[-1], num_points)
    x_smooth = np.interp(target_lengths, cumulative_length, x_dense)
    y_smooth = np.interp(target_lengths, cumulative_length, y_dense)
    
    poly_deriv = np.polyder(poly)
    gradients = poly_deriv(x_smooth)
    angles = np.arctan(gradients)
    
    return x_smooth, y_smooth, angles

def update_plot(years=None, data=None):
    if years is None:
        years = current_years
    if data is None:
        data = current_data
    
    x_numeric = np.linspace(0, 650, len(years))
    y_min, y_max = data.min(), data.max()
    y_scaled = 150 + (data - y_min) / (y_max - y_min) * 400
    
    num_lights = num_lights_slider.value
    light_size = light_size_slider.value
    
    x_smooth, y_smooth, angles = calculate_smooth_rotation_angles(
        x_numeric, y_scaled, 
        poly_degree=4,
        num_points=num_lights
    )
    
    url = light_select.value
    N = len(x_smooth)
    
    light_source.data = dict(
        url=[url]*N,
        x1=x_smooth,
        y1=y_smooth,
        w1=np.repeat(light_size, N),
        h1=np.repeat(light_size, N),
        angle=angles,
    )
    
    # Update axis labels
    tick_indices = np.arange(0, len(years), max(1, len(years)//10))
    tick_positions = x_numeric[tick_indices]
    years_str_local = [str(int(y)) for y in years]
    tick_labels = {pos: years_str_local[i] for pos, i in zip(tick_positions, tick_indices)}
    
    plot.xaxis.ticker = FixedTicker(ticks=list(tick_positions))
    plot.xaxis.major_label_overrides = tick_labels
    
    y_tick_positions = np.linspace(150, 550, 5)
    y_tick_labels = {
        pos: f"{y_min + (pos - 150) / 400 * (y_max - y_min):.2f}"
        for pos in y_tick_positions
    }
    plot.yaxis.ticker = FixedTicker(ticks=list(y_tick_positions))
    plot.yaxis.major_label_overrides = y_tick_labels

# Initial data preparation
x_numeric = np.linspace(0, 650, len(years_numeric))
y_min, y_max = temp_anomaly.min(), temp_anomaly.max()
y_scaled = 150 + (temp_anomaly - y_min) / (y_max - y_min) * 400

x_smooth, y_smooth, angles = calculate_smooth_rotation_angles(
    x_numeric, y_scaled, 
    poly_degree=4,
    num_points=15
)

# Data sources
light_source = ColumnDataSource(dict(
    url=[CLURLlist[0]]*len(x_smooth),
    x1=x_smooth,
    y1=y_smooth,
    w1=np.repeat(200, len(x_smooth)),
    h1=np.repeat(200, len(x_smooth)),
    angle=angles,
))

text_source = ColumnDataSource(dict(
    x=[325],
    y=[350],
    text=[""],
    text_color=["#ffffff"],
    text_font_size=["20pt"]
))

text_source2 = ColumnDataSource(dict(
    x=[325],
    y=[300],
    text=[""],
    text_color=["#ffffff"],
    text_font_size=["20pt"]
))

# Create plot
plot = figure(
    width=900, height=600,
    x_range=(-100, 700),
    y_range=(-100, 700),
    tools="",
)

# Add custom title
title_obj = Title(text="", text_font_size="18pt", text_color="#4A90E2", 
                  text_font_style="bold", align="center")
plot.add_layout(title_obj, 'above')

image1 = ImageURL(url="url", x="x1", y="y1", w="w1", h="h1", 
                  anchor="center", angle='angle', global_alpha=0.9)
plot.add_glyph(light_source, image1)

# Add text glyph
plot.text(x='x', y='y', text='text', text_color='text_color', 
          text_font_size='text_font_size', text_align='center',
          text_baseline='middle', source=text_source)

# Add second text glyph (always below the first)
plot.text(x='x', y='y', text='text', text_color='text_color', 
          text_font_size='text_font_size', text_align='center',
          text_baseline='middle', source=text_source2)

plot.toolbar.logo = None

# Remove borders
plot.grid.visible = False
plot.outline_line_color = None
plot.outline_line_alpha = 0
plot.outline_line_width = 0

# Set transparent background
plot.background_fill_alpha = 1
plot.border_fill_alpha = 1


# Enlarge axis labels
plot.xaxis.major_label_text_font_size = "16pt"
plot.yaxis.major_label_text_font_size = "16pt"
plot.xaxis.axis_label_text_font_size = "18pt"
plot.yaxis.axis_label_text_font_size = "18pt"

# Make axis lines invisible
plot.xaxis.axis_line_color = None
plot.yaxis.axis_line_color = None
plot.xaxis.major_tick_line_color = None
plot.yaxis.major_tick_line_color = None
plot.xaxis.minor_tick_line_color = None
plot.yaxis.minor_tick_line_color = None

# Create background div - positioned to the LEFT of the plot like original
bg_div = Div(text=f'<div style="position: absolute; left:-910px; top:0px"><img src={BGURLlist[-1]} style="width:900px; height:600px; opacity: 0.2"></div>')

# UI Controls
title_input = TextInput(title="Chart Title:", value="", placeholder="Enter chart title...", stylesheets = [textinput_css])

bg_select = Select(title="Background:", value=BGURLlist[-1], 
                   options=[(url, f"Background {i+1}") for i, url in enumerate(BGURLlist)], stylesheets = [select_css])
light_select = Select(title="Light Style:", value=CLURLlist[0],
                      options=[(url, f"Light {i+1}") for i, url in enumerate(CLURLlist)], stylesheets = [select_css])

# Climate data selector
if climate_data_available:
    climate_options = [('none', 'None (Default Data)')] + [
        (col, col.replace('_', ' ').upper()) 
        for col in climate_df.columns if col != 'year'
    ]
    climate_select = Select(
        title="Demo Climate Data:", 
        value='none',
        options=climate_options, stylesheets = [select_css]
    )
else:
    climate_select = Select(
        title="Demo Climate Data:", 
        value='none',
        options=[('none', 'Climate data not available')], stylesheets = [select_css]
    )


def climate_change(attr, old, new):
    if new == "none":
        title_obj.text = ""
    else:
        # Convert value → label
        label = dict(climate_options).get(new, new)
        title_obj.text = 'ERA5 - EUROPE - '+label
    update_plot()

# Register callback
climate_select.on_change("value", climate_change)

num_lights_slider = Slider(start=5, end=50, value=15, step=1, title="Number of Lights", stylesheets = [slider_style])
light_size_slider = Slider(start=50, end=400, value=200, step=10, title="Light Size", stylesheets = [slider_style])
bg_opacity_slider = Slider(start=0.0, end=1.0, value=0.2, step=0.05, title="Background Opacity", stylesheets = [slider_style])

text_input = TextInput(title="Text Line 1:", value="", placeholder="e.g., Merry Christmas", stylesheets = [textinput_css])
text_input2 = TextInput(title="Text Line 2:", value="", placeholder="e.g., and a Happy New Year!", stylesheets = [textinput_css])
text_x_slider = Slider(start=-100, end=700, value=325, step=5, title="Text X Position", stylesheets = [slider_style])
text_y_slider = Slider(start=-100, end=700, value=350, step=5, title="Text Y Position", stylesheets = [slider_style])
text_color_picker = ColorPicker(title="Text Color", color="#ffffff")
text_size_slider = Slider(start=10, end=60, value=20, step=2, title="Text Size", stylesheets = [slider_style])

file_input = FileInput(accept=".txt,.csv,.xls,.xlsx", stylesheets = [file_input_style])
file_status = PreText(text="No file uploaded")



# Callbacks
def title_update(attr, old, new):
    title_obj.text = new

def bg_change(attr, old, new):
    opacity = bg_opacity_slider.value
    bg_div.text = f'<div style="position: absolute; left:-910px; top:0px"><img src={new} style="width:900px; height:600px; opacity: {opacity}"></div>'

def bg_opacity_change(attr, old, new):
    current_bg = bg_select.value
    bg_div.text = f'<div style="position: absolute; left:-910px; top:0px"><img src={current_bg} style="width:900px; height:600px; opacity: {new}"></div>'

def light_change(attr, old, new):
    update_plot()

def num_lights_change(attr, old, new):
    update_plot()

def light_size_change(attr, old, new):
    update_plot()

def text_update(attr, old, new):
    text_source.data['text'] = [text_input.value]

def text_update2(attr, old, new):
    text_source2.data['text'] = [text_input2.value]

def text_x_update(attr, old, new):
    text_source.data['x'] = [new]
    text_source2.data['x'] = [new]

def text_y_update(attr, old, new):
    text_source.data['y'] = [new]
    # Automatically place second text below first (30 units below)
    text_source2.data['y'] = [new - 80]

def text_color_update(attr, old, new):
    text_source.data['text_color'] = [new]
    text_source2.data['text_color'] = [new]

def text_size_update(attr, old, new):
    text_source.data['text_font_size'] = [f"{new}pt"]
    text_source2.data['text_font_size'] = [f"{new}pt"]

def climate_data_change(attr, old, new):
    global current_years, current_data
    if new == 'none' or not climate_data_available:
        # Reset to default data
        current_years = years_numeric
        current_data = temp_anomaly
        file_status.text = "Using default data"
    else:
        # Load selected climate variable
        current_years = climate_df['year'].values
        current_data = climate_df[new].values
        file_status.text = f"✓ Loaded {new.replace('_', ' ').title()}"
    
    update_plot(current_years, current_data)

def file_upload(attr, old, new):
    global current_years, current_data
    try:
        decoded = base64.b64decode(new)
        file_content = decoded.decode('utf-8')
        
        # Try to parse as CSV/TXT
        lines = file_content.strip().split('\n')
        years_list = []
        data_list = []
        
        for line in lines[1:]:  # Skip header
            parts = line.strip().split(',') if ',' in line else line.strip().split()
            if len(parts) >= 2:
                try:
                    years_list.append(float(parts[0]))
                    data_list.append(float(parts[1]))
                except:
                    continue
        
        if len(years_list) > 0:
            current_years = np.array(years_list)
            current_data = np.array(data_list)
            update_plot(current_years, current_data)
            file_status.text = f"✓ Loaded {len(years_list)} data points from uploaded file"
            # Reset climate selector
            climate_select.value = 'none'
        else:
            file_status.text = "✗ No valid data found"
    except Exception as e:
        file_status.text = f"✗ Error: {str(e)}"

# Attach callbacks
title_input.on_change('value', title_update)
bg_select.on_change('value', bg_change)
bg_opacity_slider.on_change('value', bg_opacity_change)
light_select.on_change('value', light_change)
num_lights_slider.on_change('value', num_lights_change)
light_size_slider.on_change('value', light_size_change)
text_input.on_change('value', text_update)
text_input2.on_change('value', text_update2)
text_x_slider.on_change('value', text_x_update)
text_y_slider.on_change('value', text_y_update)
text_color_picker.on_change('color', text_color_update)
text_size_slider.on_change('value', text_size_update)
climate_select.on_change('value', climate_data_change)
file_input.on_change('value', file_upload)

# Layout - like the original with Row(plot, bg_div)
controls = Row(
    Column(title_input,
    bg_select,
    bg_opacity_slider,
    light_select,
    num_lights_slider,
    light_size_slider,
    climate_select),
    Column(
    text_input,
    text_input2,
    text_x_slider,
    text_y_slider,
    text_size_slider,
    text_color_picker,
    Div(text="<h3>Custom Data Upload</h3>"),
    file_input,
    file_status,
    ),
    width=320
)

main_layout = layout([
    [Row(plot, bg_div), controls]
],stylesheets = [gstyle])

curdoc().add_root(main_layout)
curdoc().title = "Interactive Christmas Lights Visualization"
