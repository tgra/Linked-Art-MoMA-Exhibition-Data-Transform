import Head from 'next/head'
import Link from 'next/link';

export default function Home() {
  return (
    <div className="container">
      <Head>
        <title>Alternative New York Exhibitions</title>

        
      </Head>

      <main>
        <h1 className="title">Alternative New York Exhibitions</h1>

        <p className="description">
          This is a demo visualisation of art exhibition data represented using the Linked Art data model.
        </p>

        <div className="grid">
          

          <a href="/exhibitions" className="card">
            <h3>Exhibitions</h3>
            <p><Link href="/exhibitions">Explore exhibitions</Link></p>
          </a>
          <a href="/artists" className="card">
            <h3>Artists</h3>
            <p><Link href="/artists">Explore artists</Link></p>
          </a>

          <a
            href="/exhibitions_mapped"
            className="card"
          >
            <h3>Exhibitions Mapped</h3>
            <p>Alternative New York exhibitions on a map</p>
          </a>

          <a
            href="/exhibitions_sankey"
            className="card"
          >
            <h3>Exhibitions vis.</h3>
            <p>
              Relationships between artists and exhibitions
            </p>
          </a>
        </div>
      </main>

     

    
    </div>
  )
}
