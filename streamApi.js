return (async () => {
  const generateFakeDeviceId = () => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  };

  try {
    const deviceId = generateFakeDeviceId();
    // Menggunakan identitas Dalvik agar tidak ditolak CDN
    const userAgent = 'Dalvik/2.1.0 (Linux; U; Android 10; K Build/QP1A.190711.020)';

    // 1. Minta Token Visitor Android
    const visitorRes = await fetch(`https://api.rctiplus.com/api/v1/visitor?platform=android&device_id=${deviceId}`, {
      headers: { 'User-Agent': userAgent }
    });
    const visitorData = await visitorRes.json();
    const token = visitorData?.data?.access_token;

    if (!token) return null;

    // 2. Tukar Token dengan Link M3U8
    const liveRes = await fetch(`https://toutatis.rctiplus.com/video/live/api/v1/live/1/url?appierid=${deviceId}`, {
      headers: {
        'apikey': 'jFFhGYfZzrEgaPIGmFOVttQzCNbvqJHb',
        'authorization': token,
        'User-Agent': userAgent,
        'Origin': 'https://m.rctiplus.com',
        'Referer': 'https://m.rctiplus.com/'
      }
    });
    const liveData = await liveRes.json();
    
    // Kembalikan link segar
    return liveData?.data?.url || null;

  } catch (error) {
    return null;
  }
})();
