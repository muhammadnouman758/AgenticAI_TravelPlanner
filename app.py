import gradio as gr
from planner import authenticate_google_calendar, generate_gemini_itinerary
from weather_utils import (
    fetch_weather_forecast,
    format_weather_table,
    extract_trip_days,
    generate_weather_safety_advice
)
from calender_utils import write_to_calendar, check_calendar_conflicts

# 📅 Authenticate Google Calendar
calendar_service = authenticate_google_calendar()

# 🔧 Main logic (unchanged)
def generate_plan(user_input, start_date):
    if "islamabad" not in user_input.lower():
        return (
            "Only Islamabad is currently supported.",
            "", "", ""
        )

    num_days = extract_trip_days(user_input)

    # 🌦️ Weather Forecast
    forecast = fetch_weather_forecast()
    if not forecast:
        return (
            "⚠️ Weather API error",
            "❌ Weather unavailable",
            "Trip plan unavailable",
            "Calendar skipped"
        )

    weather_table = format_weather_table(forecast, num_days)
    safety_advice = generate_weather_safety_advice(forecast, num_days)

    # ✈️ AI Itinerary
    itinerary_text, raw_schedule = generate_gemini_itinerary(user_input, start_date)

    # 🧠 First check for conflicts BEFORE writing
    conflict_info = check_calendar_conflicts(raw_schedule, start_date, calendar_service)

    # ✅ Write to calendar if needed
    write_result = write_to_calendar(raw_schedule, start_date, calendar_service)

    # 🧾 Final result
    calendar_md = f"{conflict_info}\n\n{write_result['status']}"

    return (
        f"### 🌤️ Weather Forecast\n{weather_table}",
        f"### 🛡️ Safety Advisory\n{safety_advice}",
        itinerary_text,
        calendar_md
    )

# Enhanced Custom CSS with beautiful animations and modern design
custom_css = """
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Global styling with modern gradient */
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
    background-size: 400% 400% !important;
    animation: gradientShift 15s ease infinite !important;
    min-height: 100vh;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Glass morphism main container */
.main-container {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 25px !important;
    box-shadow: 
        0 25px 45px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    margin: 20px !important;
    padding: 40px !important;
    position: relative;
    overflow: hidden;
}

.main-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    animation: shimmer 2s ease-in-out infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* Modern header with beautiful typography */
.header-title {
    background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    text-align: center !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 3.5em !important;
    font-weight: 700 !important;
    margin-bottom: 10px !important;
    text-shadow: 0 4px 20px rgba(255, 255, 255, 0.3) !important;
    letter-spacing: -0.02em !important;
}

.header-subtitle {
    text-align: center !important;
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 1.3em !important;
    margin-bottom: 40px !important;
    font-weight: 300 !important;
    line-height: 1.6 !important;
}

/* Ultra-modern input section with floating effect */
.input-section {
    background: rgba(255, 255, 255, 0.15) !important;
    border-radius: 20px !important;
    padding: 35px !important;
    margin-bottom: 40px !important;
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    position: relative;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.input-section:hover {
    transform: translateY(-5px) !important;
    box-shadow: 
        0 30px 60px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

/* Enhanced textbox styling with floating labels effect */
.input-section .gr-textbox {
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 15px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-size: 1.1em !important;
    padding: 20px !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
    position: relative !important;
}

.input-section .gr-textbox:focus {
    border-color: rgba(255, 255, 255, 0.8) !important;
    box-shadow: 
        0 0 30px rgba(255, 255, 255, 0.3),
        0 15px 35px rgba(102, 126, 234, 0.2) !important;
    transform: translateY(-3px) !important;
    background: rgba(255, 255, 255, 0.95) !important;
}

.input-section .gr-textbox textarea {
    min-height: 120px !important;
    resize: vertical !important;
    font-family: 'Inter', sans-serif !important;
    line-height: 1.6 !important;
}

/* Date input with special calendar styling */
.date-container {
    position: relative !important;
}

.date-container .gr-textbox {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 249, 255, 0.9) 100%) !important;
    border: 2px solid rgba(102, 126, 234, 0.3) !important;
}

.date-container .gr-textbox:focus {
    border-color: #667eea !important;
    box-shadow: 
        0 0 25px rgba(102, 126, 234, 0.4),
        0 10px 30px rgba(102, 126, 234, 0.2) !important;
}

/* Spectacular button with multiple gradients and animations */
.generate-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
    background-size: 300% 300% !important;
    border: none !important;
    border-radius: 18px !important;
    padding: 18px 50px !important;
    font-size: 1.2em !important;
    font-weight: 600 !important;
    color: white !important;
    cursor: pointer !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 
        0 15px 35px rgba(102, 126, 234, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    width: 100% !important;
    margin-top: 25px !important;
    position: relative !important;
    overflow: hidden !important;
    font-family: 'Poppins', sans-serif !important;
    letter-spacing: 0.5px !important;
    animation: buttonGradient 6s ease infinite !important;
}

@keyframes buttonGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.generate-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}

.generate-btn:hover::before {
    left: 100%;
}

.generate-btn:hover {
    transform: translateY(-4px) scale(1.02) !important;
    box-shadow: 
        0 25px 50px rgba(102, 126, 234, 0.6),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
}

.generate-btn:active {
    transform: translateY(-2px) scale(0.98) !important;
}

/* Ultra-modern tab styling with glassmorphism */
.tab-nav {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 20px !important;
    padding: 8px !important;
    margin-bottom: 25px !important;
    box-shadow: 
        inset 0 2px 10px rgba(0, 0, 0, 0.1),
        0 10px 30px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.tab-nav button {
    border-radius: 15px !important;
    padding: 15px 25px !important;
    margin: 3px !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-weight: 500 !important;
    color: rgba(255, 255, 255, 0.8) !important;
    font-size: 1.05em !important;
    position: relative !important;
    overflow: hidden !important;
}

.tab-nav button::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
    opacity: 0;
    transition: opacity 0.3s ease;
}

.tab-nav button:hover::before {
    opacity: 1;
}

.tab-nav button.selected {
    background: rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    box-shadow: 
        0 8px 25px rgba(255, 255, 255, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    backdrop-filter: blur(10px) !important;
}

.tab-nav button:hover:not(.selected) {
    background: rgba(255, 255, 255, 0.1) !important;
    transform: translateY(-2px) !important;
    color: white !important;
}

/* Enhanced output containers with beautiful gradients */
.output-container {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    margin: 15px 0 !important;
    box-shadow: 
        0 15px 35px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    border-left: 5px solid #667eea !important;
    position: relative !important;
    transition: all 0.4s ease !important;
}

.output-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.02), transparent);
    border-radius: 20px;
    pointer-events: none;
}

.output-container:hover {
    transform: translateY(-3px) !important;
    box-shadow: 
        0 25px 50px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
}

/* Specialized tab styling with unique gradients */
.weather-tab .output-container {
    border-left-color: #4facfe !important;
    background: linear-gradient(135deg, rgba(79, 172, 254, 0.08) 0%, rgba(255, 255, 255, 0.95) 50%) !important;
}

.safety-tab .output-container {
    border-left-color: #f5576c !important;
    background: linear-gradient(135deg, rgba(245, 87, 108, 0.08) 0%, rgba(255, 255, 255, 0.95) 50%) !important;
}

.itinerary-tab .output-container {
    border-left-color: #43e97b !important;
    background: linear-gradient(135deg, rgba(67, 233, 123, 0.08) 0%, rgba(255, 255, 255, 0.95) 50%) !important;
}

.calendar-tab .output-container {
    border-left-color: #fa709a !important;
    background: linear-gradient(135deg, rgba(250, 112, 154, 0.08) 0%, rgba(255, 255, 255, 0.95) 50%) !important;
}

/* Section headers with modern styling */
.section-header {
    color: rgba(255, 255, 255, 0.95) !important;
    font-size: 1.4em !important;
    font-weight: 600 !important;
    margin-bottom: 20px !important;
    text-align: center !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Labels with enhanced styling */
.gr-form label {
    color: rgba(255, 255, 255, 0.9) !important;
    font-weight: 500 !important;
    font-size: 1.1em !important;
    margin-bottom: 8px !important;
    display: block !important;
}

/* Info text styling */
.gr-form .gr-info {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 0.95em !important;
    font-style: italic !important;
    margin-top: 5px !important;
}

/* Loading animation enhancement */
.loading {
    display: inline-block;
    width: 24px;
    height: 24px;
    border: 3px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    border-top-color: #667eea;
    animation: spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Enhanced responsive design */
@media (max-width: 768px) {
    .main-container {
        margin: 10px !important;
        padding: 25px !important;
    }
    
    .header-title {
        font-size: 2.5em !important;
    }
    
    .input-section {
        padding: 25px !important;
    }
    
    .generate-btn {
        padding: 16px 40px !important;
        font-size: 1.1em !important;
    }
}

/* Ultra-enhanced markdown styling */
.markdown-content h3 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    border-bottom: 2px solid rgba(102, 126, 234, 0.2) !important;
    padding-bottom: 12px !important;
    margin-bottom: 20px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
}

.markdown-content table {
    border-collapse: collapse !important;
    width: 100% !important;
    margin: 20px 0 !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    background: white !important;
}

.markdown-content th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    padding: 15px !important;
    font-weight: 600 !important;
    text-align: left !important;
    font-size: 1.05em !important;
}

.markdown-content td {
    padding: 12px 15px !important;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
    transition: background 0.3s ease !important;
}

.markdown-content tr:nth-child(even) {
    background: rgba(102, 126, 234, 0.03) !important;
}

.markdown-content tr:hover {
    background: rgba(102, 126, 234, 0.08) !important;
    transform: scale(1.01) !important;
    transition: all 0.3s ease !important;
}

/* Footer styling */
.footer {
    text-align: center !important;
    color: rgba(255, 255, 255, 0.7) !important;
    margin-top: 40px !important;
    padding: 25px !important;
    border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Add floating particles effect */
.main-container::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: 
        radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
    pointer-events: none;
    border-radius: 25px;
}
"""

# 🖼️ Ultra-Enhanced UI with Gradio
with gr.Blocks(css=custom_css, title="✈️ AI Travel Planner") as demo:
    with gr.Column(elem_classes=["main-container"]):
        # Enhanced Header Section
        gr.Markdown(
            """
            # ✈️ Agentic AI Travel Planner
            ### 🏛️ Discover the Magnificent Beauty of Islamabad
            Plan your perfect journey with AI-powered insights, real-time weather intelligence, and seamless calendar integration.
            """,
            elem_classes=["header-title", "header-subtitle"]
        )
        
        # Ultra-Modern Input Section
        with gr.Group(elem_classes=["input-section"]):
            gr.Markdown("### 📝 Craft Your Dream Trip", elem_classes=["section-header"])
            
            with gr.Row():
                with gr.Column(scale=2):
                    user_input = gr.Textbox(
                        label="✍️ Describe Your Perfect Trip Experience",
                        placeholder="🌟 Share your travel dreams... e.g., 'Plan an enchanting 3-day cultural exploration in Islamabad with family-friendly adventures, historical landmarks, and authentic local cuisine experiences'",
                        lines=4,
                        info="💡 The more details you share about your preferences, interests, budget, and travel style, the more personalized your itinerary will be",
                        elem_classes=["trip-description"]
                    )
                
                with gr.Column(scale=1, elem_classes=["date-container"]):
                    with gr.Row():
                        start_date = gr.Textbox(
                            label="📅 Choose Your Adventure Start Date",
                            placeholder="Click calendar to select date",
                            info="📆 Pick your perfect travel start date",
                            elem_classes=["date-input"],
                            interactive=True
                        )
                    
                    # Advanced Calendar Interface
                    calendar_html = gr.HTML("""
                    <div id="calendar-container" style="display: none; margin-top: 10px;">
                        <div id="calendar-picker" style="
                            background: rgba(255, 255, 255, 0.95);
                            border-radius: 15px;
                            padding: 20px;
                            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
                            backdrop-filter: blur(10px);
                            border: 1px solid rgba(255, 255, 255, 0.3);
                            max-width: 350px;
                            font-family: 'Inter', sans-serif;
                        ">
                            <div id="calendar-header" style="
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                                margin-bottom: 20px;
                                padding: 0 10px;
                            ">
                                <button id="prev-month" style="
                                    background: linear-gradient(135deg, #667eea, #764ba2);
                                    border: none;
                                    color: white;
                                    width: 35px;
                                    height: 35px;
                                    border-radius: 50%;
                                    cursor: pointer;
                                    font-size: 16px;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    transition: all 0.3s ease;
                                ">‹</button>
                                <h3 id="month-year" style="
                                    margin: 0;
                                    color: #333;
                                    font-weight: 600;
                                    font-size: 1.1em;
                                "></h3>
                                <button id="next-month" style="
                                    background: linear-gradient(135deg, #667eea, #764ba2);
                                    border: none;
                                    color: white;
                                    width: 35px;
                                    height: 35px;
                                    border-radius: 50%;
                                    cursor: pointer;
                                    font-size: 16px;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    transition: all 0.3s ease;
                                ">›</button>
                            </div>
                            <div id="calendar-weekdays" style="
                                display: grid;
                                grid-template-columns: repeat(7, 1fr);
                                gap: 2px;
                                margin-bottom: 10px;
                            ">
                                <div style="text-align: center; font-weight: 600; color: #666; padding: 8px 0; font-size: 0.9em;">Sun</div>
                                <div style="text-align: center; font-weight: 600; color: #666; padding: 8px 0; font-size: 0.9em;">Mon</div>
                                <div style="text-align: center; font-weight: 600; color: #666; padding: 8px 0; font-size: 0.9em;">Tue</div>
                                <div style="text-align: center; font-weight: 600; color: #666; padding: 8px 0; font-size: 0.9em;">Wed</div>
                                <div style="text-align: center; font-weight: 600; color: #666; padding: 8px 0; font-size: 0.9em;">Thu</div>
                                <div style="text-align: center; font-weight: 600; color: #666; padding: 8px 0; font-size: 0.9em;">Fri</div>
                                <div style="text-align: center; font-weight: 600; color: #666; padding: 8px 0; font-size: 0.9em;">Sat</div>
                            </div>
                            <div id="calendar-days" style="
                                display: grid;
                                grid-template-columns: repeat(7, 1fr);
                                gap: 3px;
                            "></div>
                            <div style="
                                margin-top: 15px;
                                padding-top: 15px;
                                border-top: 1px solid rgba(0, 0, 0, 0.1);
                                display: flex;
                                justify-content: space-between;
                            ">
                                <button id="today-btn" style="
                                    background: linear-gradient(135deg, #43e97b, #38d9a9);
                                    border: none;
                                    color: white;
                                    padding: 8px 16px;
                                    border-radius: 8px;
                                    cursor: pointer;
                                    font-size: 0.9em;
                                    font-weight: 500;
                                    transition: all 0.3s ease;
                                ">Today</button>
                                <button id="close-calendar" style="
                                    background: linear-gradient(135deg, #f5576c, #f093fb);
                                    border: none;
                                    color: white;
                                    padding: 8px 16px;
                                    border-radius: 8px;
                                    cursor: pointer;
                                    font-size: 0.9em;
                                    font-weight: 500;
                                    transition: all 0.3s ease;
                                ">Close</button>
                            </div>
                        </div>
                    </div>
                    
                    <script>
                    (function() {
                        let currentDate = new Date();
                        let selectedDate = null;
                        
                        const monthNames = [
                            'January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December'
                        ];
                        
                        function renderCalendar() {
                            const monthYear = document.getElementById('month-year');
                            const calendarDays = document.getElementById('calendar-days');
                            
                            if (!monthYear || !calendarDays) return;
                            
                            monthYear.textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
                            
                            const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
                            const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
                            const startDate = new Date(firstDay);
                            startDate.setDate(startDate.getDate() - firstDay.getDay());
                            
                            calendarDays.innerHTML = '';
                            
                            for (let i = 0; i < 42; i++) {
                                const date = new Date(startDate);
                                date.setDate(startDate.getDate() + i);
                                
                                const dayElement = document.createElement('div');
                                dayElement.textContent = date.getDate();
                                dayElement.style.cssText = `
                                    text-align: center;
                                    padding: 10px 5px;
                                    cursor: pointer;
                                    border-radius: 8px;
                                    transition: all 0.3s ease;
                                    font-size: 0.95em;
                                    font-weight: 500;
                                    position: relative;
                                    user-select: none;
                                `;
                                
                                const today = new Date();
                                const isToday = date.toDateString() === today.toDateString();
                                const isCurrentMonth = date.getMonth() === currentDate.getMonth();
                                const isPast = date < today && !isToday;
                                
                                if (isToday) {
                                    dayElement.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
                                    dayElement.style.color = 'white';
                                    dayElement.style.fontWeight = '600';
                                } else if (!isCurrentMonth) {
                                    dayElement.style.color = '#ccc';
                                    dayElement.style.cursor = 'not-allowed';
                                } else if (isPast) {
                                    dayElement.style.color = '#999';
                                    dayElement.style.cursor = 'not-allowed';
                                } else {
                                    dayElement.style.color = '#333';
                                }
                                
                                if (selectedDate && date.toDateString() === selectedDate.toDateString()) {
                                    dayElement.style.background = 'linear-gradient(135deg, #43e97b, #38d9a9)';
                                    dayElement.style.color = 'white';
                                    dayElement.style.fontWeight = '600';
                                }
                                
                                dayElement.addEventListener('mouseenter', function() {
                                    if (isCurrentMonth && !isPast) {
                                        this.style.background = 'linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1))';
                                        this.style.transform = 'scale(1.1)';
                                    }
                                });
                                
                                dayElement.addEventListener('mouseleave', function() {
                                    if (!selectedDate || date.toDateString() !== selectedDate.toDateString()) {
                                        if (isToday) {
                                            this.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
                                        } else {
                                            this.style.background = 'transparent';
                                        }
                                    }
                                    this.style.transform = 'scale(1)';
                                });
                                
                                dayElement.addEventListener('click', function() {
                                    if (isCurrentMonth && !isPast) {
                                        selectedDate = new Date(date);
                                        const formattedDate = selectedDate.getFullYear() + '-' + 
                                            String(selectedDate.getMonth() + 1).padStart(2, '0') + '-' + 
                                            String(selectedDate.getDate()).padStart(2, '0');
                                        
                                        const dateInput = document.querySelector('.date-input input');
                                        if (dateInput) {
                                            dateInput.value = formattedDate;
                                            dateInput.dispatchEvent(new Event('input', { bubbles: true }));
                                        }
                                        
                                        renderCalendar();
                                        
                                        // Auto-close calendar after selection
                                        setTimeout(() => {
                                            const calendarContainer = document.getElementById('calendar-container');
                                            if (calendarContainer) {
                                                calendarContainer.style.display = 'none';
                                            }
                                        }, 300);
                                    }
                                });
                                
                                calendarDays.appendChild(dayElement);
                            }
                        }
                        
                        // Event listeners
                        document.addEventListener('click', function(e) {
                            const dateInput = e.target.closest('.date-input');
                            const calendarContainer = document.getElementById('calendar-container');
                            
                            if (dateInput && !e.target.closest('#calendar-container')) {
                                if (calendarContainer) {
                                    calendarContainer.style.display = calendarContainer.style.display === 'none' ? 'block' : 'none';
                                    if (calendarContainer.style.display === 'block') {
                                        renderCalendar();
                                    }
                                }
                            } else if (!e.target.closest('#calendar-container') && !dateInput) {
                                if (calendarContainer) {
                                    calendarContainer.style.display = 'none';
                                }
                            }
                        });
                        
                        document.getElementById('prev-month')?.addEventListener('click', function() {
                            currentDate.setMonth(currentDate.getMonth() - 1);
                            renderCalendar();
                        });
                        
                        document.getElementById('next-month')?.addEventListener('click', function() {
                            currentDate.setMonth(currentDate.getMonth() + 1);
                            renderCalendar();
                        });
                        
                        document.getElementById('today-btn')?.addEventListener('click', function() {
                            const today = new Date();
                            selectedDate = today;
                            currentDate = new Date(today);
                            const formattedDate = today.getFullYear() + '-' + 
                                String(today.getMonth() + 1).padStart(2, '0') + '-' + 
                                String(today.getDate()).padStart(2, '0');
                            
                            const dateInput = document.querySelector('.date-input input');
                            if (dateInput) {
                                dateInput.value = formattedDate;
                                dateInput.dispatchEvent(new Event('input', { bubbles: true }));
                            }
                            renderCalendar();
                        });
                        
                        document.getElementById('close-calendar')?.addEventListener('click', function() {
                            const calendarContainer = document.getElementById('calendar-container');
                            if (calendarContainer) {
                                calendarContainer.style.display = 'none';
                            }
                        });
                        
                        // Initialize calendar
                        setTimeout(renderCalendar, 100);
                    })();
                    </script>
                    """)
            
            gen_btn = gr.Button(
                "🚀 Create My Magical Travel Experience",
                elem_classes=["generate-btn"],
                variant="primary",
                size="lg"
            )
        
        # Enhanced Results Section with Beautiful Tabs
        gr.Markdown("### 📊 Your Personalized Travel Masterpiece", elem_classes=["results-header"])
        
        with gr.Tabs(elem_classes=["tab-nav"]) as tabs:
            with gr.Tab("🌤️ Weather Intelligence", elem_classes=["weather-tab"]):
                with gr.Column(elem_classes=["output-container"]):
                    gr.Markdown("🌡️ **Real-time Weather Insights** - Get comprehensive weather forecasting to plan your activities with confidence and make the most of every moment.")
                    weather_output = gr.Markdown(elem_classes=["markdown-content"])
            
            with gr.Tab("🛡️ Smart Safety Guide", elem_classes=["safety-tab"]):
                with gr.Column(elem_classes=["output-container"]):
                    gr.Markdown("⚡ **Intelligent Safety Recommendations** - Receive personalized safety tips and weather-based precautions to ensure your journey is both amazing and secure.")
                    safety_output = gr.Markdown(elem_classes=["markdown-content"])
            
            with gr.Tab("📋 Curated Itinerary", elem_classes=["itinerary-tab"]):
                with gr.Column(elem_classes=["output-container"]):
                    gr.Markdown("🎯 **Your Personal Travel Blueprint** - Discover a meticulously crafted day-by-day itinerary with perfect timing, must-visit locations, and hidden gems.")
                    itinerary_output = gr.Markdown(elem_classes=["markdown-content"])
            
            with gr.Tab("📆 Calendar Harmony", elem_classes=["calendar-tab"]):
                with gr.Column(elem_classes=["output-container"]):
                    gr.Markdown("🔄 **Seamless Schedule Integration** - Automatic calendar synchronization with intelligent conflict detection for effortless trip planning.")
                    calendar_output = gr.Markdown(elem_classes=["markdown-content"])
        
        # Enhanced Footer
        gr.Markdown(
            """
            ---
            <div style="text-align: center; padding: 30px;">
                <p style="font-size: 1.1em; margin-bottom: 15px;">
                    🤖 <strong>Powered by Advanced AI</strong> | 🌐 <strong>Real-time Weather Intelligence</strong> | 📅 <strong>Google Calendar Integration</strong>
                </p>
                <p style="font-style: italic; opacity: 0.8;">
                    <em>🏛️ Currently featuring the beautiful city of Islamabad, Pakistan</em><br>
                    <em>🌍 More incredible destinations coming soon to your travel planning experience!</em>
                </p>
            </div>
            """,
            elem_classes=["footer"]
        )

    # Event Handler (unchanged functionality)
    gen_btn.click(
        generate_plan,
        inputs=[user_input, start_date],
        outputs=[weather_output, safety_output, itinerary_output, calendar_output]
    )

# Launch with enhanced settings
demo.launch()
