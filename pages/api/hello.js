// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export default async function handler(req, res) {
  async function get() {
    const info = await fetch('http://127.0.0.1:5000/test', {
      method: 'GET',
    }).then(res => res.json())
    return info
  }
  const resp = await get()
  res.send(resp)
}
