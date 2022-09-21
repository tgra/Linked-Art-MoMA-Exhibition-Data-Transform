import type { NextApiRequest, NextApiResponse } from 'next'

var fs = require('fs');

export default function eventHandler(req: NextApiRequest, res: NextApiResponse) {
  const {
    query: { id },
    method,
  } = req

  switch (method) {
    case 'GET':
        let dir = "data/event";
        let filepath = dir + '/' + id + '.json';
        console.log(filepath);
        let rawdata = fs.readFileSync(filepath);
        let event = JSON.parse(rawdata);
        res.status(200).json(event)
      break
    
    default:
      res.setHeader('Allow', ['GET', 'PUT'])
      res.status(405).end(`Method ${method} Not Allowed`)
  }
}
