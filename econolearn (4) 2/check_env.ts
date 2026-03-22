import { execSync } from 'child_process';
try {
  const pythonVersion = execSync('python3 --version').toString();
  console.log('Python version:', pythonVersion);
  const pipVersion = execSync('pip3 --version').toString();
  console.log('Pip version:', pipVersion);
  const streamlitVersion = execSync('python3 -m streamlit --version').toString();
  console.log('Streamlit version:', streamlitVersion);
} catch (e) {
  console.log('Error checking python/streamlit:', e.message);
}
