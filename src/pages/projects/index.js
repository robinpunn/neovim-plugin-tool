import { graphql, Link } from 'gatsby'
import React from 'react'
import Layout from '../../components/Layout'
import {portfolio, projects} from '../../styles/projects.module.css'
import {GatsbyImage, getImage} from 'gatsby-plugin-image'

export default function Project({ data }) {
  console.log(data)
  const getProjects = data.projects.nodes
  const contact = data.contact.siteMetadata.contact

  return (
    <Layout>
        <div className={portfolio}>
          <h2>Portfolio</h2>
          <h3>Projects and Websites I've Created</h3>
          <div className={projects}>
            {getProjects.map(getProject=> (
                <div>
                  <Link to={"/projectsText/" + getProject.frontmatter.slug} key={getProject.id}>
                    <GatsbyImage
                      image={getImage(getProject.frontmatter.thumb)}
                      alt={getProject.frontmatter.slug}
                      layout="fluid"
                      />
                  </Link>
                  <h3>{getProject.frontmatter.title}</h3>
                  <p>{ getProject.frontmatter.stack}</p>
                </div>

            ))}
          </div>
          <p>Conatact me at {contact} for more information.</p>
      </div>
    </Layout>
  )
}

// export page query
export const query = graphql`
  query ProjectsPage {
    projects: allMarkdownRemark(sort: {fields: frontmatter___date, order: ASC}) {
      nodes {
        frontmatter {
          title
          stack
          slug
          thumb {
            childImageSharp {
              gatsbyImageData(
                width: 200
                height: 200
                blurredOptions: {width: 100}
                placeholder: BLURRED
                transformOptions: {cropFocus: CENTER}
                aspectRatio: 0.7
              )
            }  
          }
        }
        id
      }
    }
    contact: site {
      siteMetadata {
        contact
      }
    }
  }
`