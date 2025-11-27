#!/usr/bin/env node
/**
 * MCP Documentation Server Wrapper
 * 
 * This wrapper allows the Python MCP server to be run via npx.
 * It automatically manages Docker containers and runs the server in Docker.
 */

const { spawn, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where this script is located
const scriptDir = __dirname;
const projectRoot = path.resolve(scriptDir, '..');
const dockerComposePath = path.join(projectRoot, 'docker-compose.yml');
const containerName = 'mcp-documentation-server';

/**
 * Check if Docker is installed and available
 */
function checkDockerAvailable() {
  try {
    execSync('docker --version', { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Check if Docker daemon is running
 */
function checkDockerDaemon() {
  try {
    execSync('docker info', { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Check if containers are running
 */
function checkContainersRunning() {
  try {
    const output = execSync(`docker ps --filter "name=${containerName}" --format "{{.Names}}"`, { encoding: 'utf-8' });
    return output.trim() === containerName;
  } catch (e) {
    return false;
  }
}

/**
 * Check if Docker images exist
 */
function checkImagesExist() {
  try {
    // Try to check if the image exists by inspecting it
    // The image name is based on the project directory name or can be checked via docker compose
    execSync('docker compose config --services', {
      cwd: projectRoot,
      stdio: 'ignore'
    });
    // If config works, try to see if images are built
    // We'll attempt build if containers can't start, so this is just a hint
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Build Docker images
 */
function buildDockerImages() {
  console.error('Building Docker images...');
  try {
    execSync('docker compose build', {
      cwd: projectRoot,
      stdio: 'inherit'
    });
    return true;
  } catch (e) {
    console.error('Error building Docker images:', e.message);
    return false;
  }
}

/**
 * Start Docker containers
 */
function startDockerContainers() {
  console.error('Starting Docker containers...');
  try {
    execSync('docker compose up -d', {
      cwd: projectRoot,
      stdio: 'inherit'
    });
    // Wait a bit for containers to start
    const maxAttempts = 30;
    let attempts = 0;
    while (attempts < maxAttempts) {
      if (checkContainersRunning()) {
        return true;
      }
      attempts++;
      // Wait 1 second
      try {
        execSync('sleep 1', { stdio: 'ignore' });
      } catch (e) {
        // sleep command might not be available on Windows, use alternative
        const start = Date.now();
        while (Date.now() - start < 1000) {
          // Busy wait
        }
      }
    }
    return false;
  } catch (e) {
    console.error('Error starting Docker containers:', e.message);
    return false;
  }
}

/**
 * Run server in Docker container
 */
function runServerInContainer() {
  const cmd = [
    'docker', 'exec', '-i', containerName,
    'python', 'src/server.py'
  ];

  const dockerProcess = spawn(cmd[0], cmd.slice(1), {
    stdio: 'inherit',
    cwd: projectRoot
  });

  // Handle process errors
  dockerProcess.on('error', (error) => {
    console.error(`Error running server in container: ${error.message}`);
    process.exit(1);
  });

  // Forward exit code
  dockerProcess.on('exit', (code, signal) => {
    if (signal) {
      process.exit(1);
    } else {
      process.exit(code || 0);
    }
  });

  // Handle signals
  process.on('SIGINT', () => {
    dockerProcess.kill('SIGINT');
  });

  process.on('SIGTERM', () => {
    dockerProcess.kill('SIGTERM');
  });
}

/**
 * Main execution
 */
async function main() {
  // Check if docker-compose.yml exists
  if (!fs.existsSync(dockerComposePath)) {
    console.error(`Error: docker-compose.yml not found at ${dockerComposePath}`);
    console.error('Please ensure you are running from the project root directory.');
    process.exit(1);
  }

  // Check Docker availability
  if (!checkDockerAvailable()) {
    console.error('Error: Docker is not installed or not found in PATH');
    console.error('');
    console.error('Please install Docker:');
    console.error('  - macOS: https://docs.docker.com/desktop/install/mac-install/');
    console.error('  - Linux: https://docs.docker.com/engine/install/');
    console.error('  - Windows: https://docs.docker.com/desktop/install/windows-install/');
    process.exit(1);
  }

  // Check Docker daemon
  if (!checkDockerDaemon()) {
    console.error('Error: Docker daemon is not running');
    console.error('');
    console.error('Please start Docker Desktop or Docker daemon:');
    console.error('  - macOS/Windows: Start Docker Desktop application');
    console.error('  - Linux: sudo systemctl start docker');
    process.exit(1);
  }

  // Check if containers are running
  if (!checkContainersRunning()) {
    // Check if images exist, if not build them
    if (!checkImagesExist()) {
      console.error('Docker images not found. Building images...');
      if (!buildDockerImages()) {
        console.error('Failed to build Docker images');
        process.exit(1);
      }
    }

    // Start containers
    if (!startDockerContainers()) {
      console.error('Failed to start Docker containers');
      process.exit(1);
    }
  }

  // Run server in container
  runServerInContainer();
}

// Run main function
main().catch((error) => {
  console.error('Unexpected error:', error);
  process.exit(1);
});
