import { useRouter } from 'next/router';
import Link from 'next/link';
import Head from 'next/head';
import type { Event } from '../../interfaces'
import useSwr from 'swr'

const fetcher = (url: string) => fetch(url).then((res) => res.json())


const Exhibition = () => {
  const router = useRouter();
  const id = router.query;
  const { data, error } = useSwr<Event[]>('/api/event/' + id.id, fetcher)

  if (error) return <div>Failed to load exhibitions</div>
  if (!data) return <div>Loading...</div>
  
  console.log(data)
  // get file contents using id and api 

  return (
    <div className="container">
    <div></div>
        <div><Link href="/">Back to home</Link> / <Link href="/exhibition">Exhibitions</Link></div>
      <Head>
        <title> Alternative New York Exhibition</title>
        
      
      </Head>


      <main>
        <h2>Title</h2>
        <h3>{data._label}</h3>
        <h2>Date</h2>
        <p>Start: {data.timespan.begin_of_the_begin}   End: {data.timespan.end_of_the_end}</p>
        <h2>Location</h2>
        <p>{data.took_place_at[0]._label}</p>
        <h3>Persons Associated with Exhibition</h3>

        <ol>
        {
        data.part[0].involved[0].about.map((person) => (
          <li key={person.id}>{person._label}</li>
        ))
      }

      </ol>
     
        </main>
        </div>


  )
}

export default Exhibition

