module.exports = {
  apps: [
    {
      name: 'flask-server',
      script: 'deployer.py',

      interpreter: 'python3',  // Ensure this matches your Python version
      instances: 1,           // Number of instances to run
      autorestart: true,      // Restart the app if it crashes
      watch: false,           // Set to true if you want to watch for file changes
      max_memory_restart: '1G', // Restart if the app uses more than 1 GB of memory
    }
  ]
}

