const fs = require('fs');
const path = require('path');

// Configuration
const ignoreDirs = ['node_modules', '.git', 'dist', 'build', 'coverage', 'tests', 'alembic', '__pycache__', 'migrations'];
const ignoreExts = ['.log', '.env', '.DS_Store', '.gitignore', '.pyc', '.pyo', '.pyd', '.pyw', '.pyz', '.pywz', '.pyzw', '.pyz', '.db'];
const maxFileSizeInBytes = 1024 * 1024; // 1MB limit per file

function collectFiles(directory) {
  const results = [];
  
  function scanDirectory(currentPath, relativePath = '') {
    const files = fs.readdirSync(currentPath);
    
    for (const file of files) {
      const fullPath = path.join(currentPath, file);
      const stats = fs.statSync(fullPath);
      const relPath = path.join(relativePath, file);
      
      if (stats.isDirectory()) {
        if (!ignoreDirs.includes(file)) {
          scanDirectory(fullPath, relPath);
        }
      } else {
        const ext = path.extname(file);
        if (!ignoreExts.includes(ext) && stats.size <= maxFileSizeInBytes) {
          try {
            const content = fs.readFileSync(fullPath, 'utf8');
            results.push({
              path: relPath,
              content
            });
          } catch (err) {
            console.error(`Error reading file ${fullPath}: ${err.message}`);
          }
        }
      }
    }
  }
  
  scanDirectory(directory);
  return results;
}

// Get the current directory
const rootDir = process.cwd();
const files = collectFiles(rootDir);

// Save results to a JSON file
const outputFile = path.join(rootDir, 'backend-files.json');
fs.writeFileSync(outputFile, JSON.stringify(files, null, 2));

console.log(`Collected ${files.length} files. Results saved to ${outputFile}`);