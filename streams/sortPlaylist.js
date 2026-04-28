const fs = require('fs');

// Pastikan nama file ini sesuai dengan file aslimu
const inputFile = 'playlist_super.m3u'; 
const outputFile = 'playlist_super_reordered.m3u';

console.log('Membaca file playlist...');
const m3uText = fs.readFileSync(inputFile, 'utf-8');
const lines = m3uText.split(/\r?\n/);

let outputLines = [];
let currentBlock = [];
let currentUrls = [];

const flushBlock = () => {
  if (currentBlock.length > 0 || currentUrls.length > 0) {
    // Urutkan URL: .m3u8 selalu di atas, sisanya di bawah
    currentUrls.sort((a, b) => {
      const isHlsA = a.includes('.m3u8');
      const isHlsB = b.includes('.m3u8');
      if (isHlsA && !isHlsB) return -1; // A naik
      if (!isHlsA && isHlsB) return 1;  // B naik
      return 0; // Tetap
    });

    // Masukkan tag info ke output (#EXTINF, #KODIPROP, dll)
    currentBlock.forEach(line => outputLines.push(line));
    // Masukkan URL yang sudah diurutkan ke output
    currentUrls.forEach(url => outputLines.push(url));

    // Bersihkan penampung untuk channel berikutnya
    currentBlock = [];
    currentUrls = [];
  }
};

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trim();
  if (!line) continue;

  if (line === '#EXTM3U') {
    outputLines.push(line);
    continue;
  }

  // Jika kita ketemu tag '#' baru tapi sudah punya URL sebelumnya,
  // berarti ini adalah channel baru. Kita flush (simpan) yang lama dulu.
  if (line.startsWith('#')) {
    if (currentUrls.length > 0) {
      flushBlock();
    }
    currentBlock.push(line);
  } 
  // Kalau itu link, masukkan ke penampung URL
  else if (line.startsWith('http')) {
    currentUrls.push(line);
  } 
  // Baris aneh lainnya (kalau ada)
  else {
    currentBlock.push(line);
  }
}

// Simpan sisa channel terakhir
flushBlock();

// Tulis ke file baru
fs.writeFileSync(outputFile, outputLines.join('\n'));
console.log(`✅ Selesai bro! File baru berhasil dibuat: ${outputFile}`);
