#!/bin/bash
#
# AURORA Project Runner
# Starts FastAPI backend and React frontend in parallel, then opens browser.
#

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Get project root directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
BACKEND_DIR="$PROJECT_ROOT/aurora-backend"
FRONTEND_DIR="$PROJECT_ROOT/aurora-frontend"

print_status() {
    echo -e "${BLUE}${BOLD}[AURORA]${NC} $1"
}

print_success() {
    echo -e "${GREEN}${BOLD}[AURORA]${NC} $1"
}

print_error() {
    echo -e "${RED}${BOLD}[AURORA]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}${BOLD}[AURORA]${NC} $1"
}

# Check requirements
check_requirements() {
    print_status "Checking requirements..."
    
    # Check if backend venv exists
    if [ ! -d "$BACKEND_DIR/venv" ]; then
        print_error "Backend virtual environment not found!"
        print_warning "Please run setup first: cd aurora-backend && python3 -m venv venv"
        exit 1
    fi
    
    # Check if frontend node_modules exists
    if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
        print_error "Frontend dependencies not installed!"
        print_warning "Please run: cd aurora-frontend && npm install"
        exit 1
    fi
    
    print_success "All requirements met!"
}

# Cleanup function
cleanup() {
    print_warning "Stopping all services..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        print_warning "Stopping Backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        print_warning "Stopping Frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    print_success "All services stopped. Goodbye!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo "============================================================"
    print_status "AURORA Project Runner"
    echo "============================================================"
    echo ""
    
    # Check requirements
    check_requirements
    echo ""
    
    # Start backend
    print_status "Starting FastAPI backend on http://localhost:8000..."
    cd "$BACKEND_DIR"
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
    python main.py > /tmp/aurora-backend.log 2>&1 &
    BACKEND_PID=$!
    cd "$PROJECT_ROOT"
    
    if [ -z "$BACKEND_PID" ]; then
        print_error "Failed to start backend!"
        exit 1
    fi
    
    print_success "Backend started (PID: $BACKEND_PID)"
    sleep 2
    
    # Start frontend
    print_status "Starting React frontend on http://localhost:3000..."
    cd "$FRONTEND_DIR"
    npm run dev > /tmp/aurora-frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd "$PROJECT_ROOT"
    
    if [ -z "$FRONTEND_PID" ]; then
        print_error "Failed to start frontend!"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    
    print_success "Frontend started (PID: $FRONTEND_PID)"
    sleep 3
    
    # Wait for frontend to be ready (simple check)
    print_status "Waiting for frontend to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_success "Frontend is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Frontend may not be ready yet, but opening browser anyway..."
        else
            sleep 1
        fi
    done
    
    # Open browser
    print_success "Opening browser at http://localhost:3000..."
    sleep 2
    
    # Detect OS and open browser
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open http://localhost:3000
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        xdg-open http://localhost:3000 2>/dev/null || sensible-browser http://localhost:3000 2>/dev/null
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows (Git Bash)
        start http://localhost:3000
    else
        print_warning "Cannot automatically open browser. Please open http://localhost:3000 manually"
    fi
    
    echo ""
    echo "============================================================"
    print_success "Services are running!"
    print_status "  Backend:  http://localhost:8000"
    print_status "  Frontend: http://localhost:3000"
    echo "============================================================"
    echo ""
    print_warning "Press Ctrl+C to stop all services"
    echo ""
    print_status "Backend logs: tail -f /tmp/aurora-backend.log"
    print_status "Frontend logs: tail -f /tmp/aurora-frontend.log"
    echo ""
    
    # Wait for user interrupt
    wait
}

# Run main function
main

