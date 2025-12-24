#!/bin/bash
# สคริปต์อัปเดต Streamlit จาก student_view.py เป็น Home.py

echo "🔄 Starting Streamlit Update Process..."
echo "============================================"

# ตรวจสอบว่าอยู่ในโฟลเดอร์ที่ถูกต้อง
if [ ! -f "Home.py" ]; then
    echo "❌ Error: Home.py not found!"
    echo "Please run this script from the Project_AI_Grader directory"
    exit 1
fi

echo "✅ Found Home.py"

# หา process streamlit ที่รันอยู่
echo "🔍 Checking for running Streamlit processes..."
STREAMLIT_PID=$(ps aux | grep '[s]treamlit run' | awk '{print $2}')

if [ -n "$STREAMLIT_PID" ]; then
    echo "⏹️  Stopping Streamlit (PID: $STREAMLIT_PID)..."
    kill $STREAMLIT_PID
    sleep 2
    
    # ตรวจสอบว่าหยุดแล้วจริงๆ
    if ps -p $STREAMLIT_PID > /dev/null 2>&1; then
        echo "⚠️  Process still running, force killing..."
        kill -9 $STREAMLIT_PID
        sleep 1
    fi
    echo "✅ Streamlit stopped"
else
    echo "ℹ️  No running Streamlit process found"
fi

# ตรวจสอบ Virtual Environment
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  No virtual environment found, using system Python"
fi

# ตรวจสอบว่ามี Streamlit ติดตั้งหรือไม่
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found! Installing..."
    pip install streamlit
fi

# เริ่มรัน Streamlit ใหม่แบบ background
echo "🚀 Starting Streamlit with Home.py..."
nohup streamlit run Home.py --server.port=8501 --server.address=0.0.0.0 > streamlit.log 2>&1 &

NEW_PID=$!
sleep 3

# ตรวจสอบว่ารันสำเร็จ
if ps -p $NEW_PID > /dev/null 2>&1; then
    echo "✅ Streamlit started successfully!"
    echo "📝 Process ID: $NEW_PID"
    echo "📊 Port: 8501"
    echo "📄 Log file: streamlit.log"
    echo ""
    echo "🌐 Access your app at: http://your-server-ip:8501"
    echo "   or: https://project-ai.triamudomsouth.ac.th"
    echo ""
    echo "📋 To view logs: tail -f streamlit.log"
    echo "⏹️  To stop: kill $NEW_PID"
else
    echo "❌ Failed to start Streamlit"
    echo "📄 Check log file: cat streamlit.log"
    exit 1
fi

echo "============================================"
echo "✅ Update completed!"
