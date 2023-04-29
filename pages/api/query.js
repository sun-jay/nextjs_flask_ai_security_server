import axios from 'axios';

export default async function handler(req, res) {
  const { time } = req.query;
  const apiUrl = `http://127.0.0.1:5000/query?time=${time}`
  cono

  try {
    const response = await axios({
      method: 'get',
      url: apiUrl,
      responseType: 'stream'
    });

    res.setHeader('Content-Type', 'video/mp4');
    res.setHeader('Content-Disposition', `attachment; filename=${time}.mp4`);

    response.data.pipe(res);
  } catch (error) {
    console.error(error);
    res.status(500).send(error.message);
  }
}
