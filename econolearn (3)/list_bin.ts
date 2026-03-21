import { execSync } from 'child_process';
try {
  const bin = execSync('ls /usr/bin').toString();
  console.log('Bin:', bin);
} catch (e) {
  console.log('Error listing /usr/bin:', e.message);
}
