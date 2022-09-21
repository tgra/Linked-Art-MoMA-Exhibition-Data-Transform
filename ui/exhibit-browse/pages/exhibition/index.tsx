import type { Event } from '../../interfaces'
import useSwr from 'swr'
import Link from 'next/link'
import Head from 'next/head'


const fetcher = (url: string) => fetch(url).then((res) => res.json())

export default function Index() {
  const { data, error } = useSwr<Event[]>('/api/events', fetcher)

  //console.log(data)
  if (error) return <div>Failed to load exhibitions</div>
  if (!data) return <div>Loading...</div>

  return (
    <div className="container">
    <div></div>
        <div><Link href="/">Back to home</Link></div>
      <Head>
        <title> Alternative New York Exhibitions</title>
        
      
      </Head>


      <div>
        <h1 className="title">Exhibitions</h1>

        <p className="description">
          List of alternative New York exhibitions
        </p>
        <ol>
      {
      data.result.map((event) => (
        <li key={event.id}>
        <Link href="/exhibition/[id]" as={`/exhibition/${event.id}`}>{event.label}</Link>
      </li>
      ))}
    </ol>
      
        <div className="grid"/>
         
       
      </div>

  
    </div>


    
  )
}