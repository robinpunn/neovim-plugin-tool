import { graphql, Link } from 'gatsby'
import React from 'react'
import Layout from '../../components/Layout'
import {portfolio, projects} from '../../styles/projects.module.css'

export default function Project({ data }) {
  console.log(data)
  const getProjects = data.allMarkdownRemark.nodes

  return (
    <Layout>
      <div className={portfolio}>
          <h2>Portfolio</h2>
          <h3>Projects and Websites I've Created</h3>
          <div className={projects}>
            {getProjects.map(getProjects=> (
              <Link to={"/projectsText/" + getProjects.frontmatter.slug} key={getProjects.id}>
                <div>
                  <h3>{getProjects.frontmatter.title}</h3>
                  <p>{ getProjects.frontmatter.stack}</p>
                </div>
              </Link>
            ))}
          </div>
      </div>
    </Layout>
  )
}

// export page query
export const query = graphql`
  query ProjectsPage {
    allMarkdownRemark(sort: {fields: frontmatter___date, order: ASC}) {
      nodes {
        frontmatter {
          title
          stack
          slug
        }
        id
      }
    }
  }
`