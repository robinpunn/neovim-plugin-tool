import { Link } from "gatsby"
import React from "react"
import Layout from "../components/Layout"
import { header, btn } from '../styles/home.module.css'
import {StaticImage} from "gatsby-plugin-image"

export default function Home() {
  
  return (
    <Layout>
      <section className={header}>
        <div>
          <h2>Learn</h2>
          <h3>Develop & Deploy</h3>
          <p>Web developer based in Illinois.</p>
          <Link className={btn} to="/projects">My Web3 Portfolio</Link>
        </div>
        <div className="imageHome">
          <StaticImage
            src="../images/banner2.png"
            alt=""
            layout="fullWidth"
            style={{ border: "2px  purple", boxShadow: "5px 5px 5px #eee, -5px -5px 5px #ffffff" }}
          />
        </div>
      </section>
    </Layout>
  )
}

