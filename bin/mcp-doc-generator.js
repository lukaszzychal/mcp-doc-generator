#!/usr/bin/env node
/**
 * MCP Documentation Server Wrapper
 * 
 * This wrapper allows the Python MCP server to be run via npx.
 * It checks for Python, sets up the environment, and runs the server in stdio mode.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where this script is located
const scriptDir = __dirname;
const projectRoot = path.resolve(scriptDir, '..');
const serverPath = path.join(projectRoot, 'src', 'server.py');

// Check if Python is available
function findPython() {
  const pythonCommands = ['python3', 'python'];
  
  for (const cmd of pythonCommands) {
    try {
      const result = require('child_process').execSync(`which ${cmd}`, { encoding: 'utf-8' }).trim();
      if (result) {
        return cmd;
      }
    } catch (e) {
      // Command not found, try next
    }
  }
  
  return null;
}

// Check if server.py exists
if (!fs.existsSync(serverPath)) {
  console.error(`Error: Server file not found at ${serverPath}`);
  process.exit(1);
}

// Find Python
const pythonCmd = findPython();
if (!pythonCmd) {
  console.error('Error: Python 3.10+ is required but not found in PATH');
  console.error('Please install Python 3.10 or later and ensure it is in your PATH');
  process.exit(1);
}

// Set up environment variables
const env = {
  ...process.env,
  PYTHONPATH: projectRoot,
  PYTHONUNBUFFERED: '1'
};

// If PLANTUML_SERVER is not set, try to use default
if (!env.PLANTUML_SERVER) {
  env.PLANTUML_SERVER = 'http://localhost:8080';
}

// Spawn Python process
const pythonProcess = spawn(pythonCmd, [serverPath], {
  stdio: 'inherit',
  env: env,
  cwd: projectRoot
});

// Handle process errors
pythonProcess.on('error', (error) => {
  console.error(`Error spawning Python process: ${error.message}`);
  process.exit(1);
});

// Forward exit code
pythonProcess.on('exit', (code, signal) => {
  if (signal) {
    process.exit(1);
  } else {
    process.exit(code || 0);
  }
});

// Handle signals
process.on('SIGINT', () => {
  pythonProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
});

