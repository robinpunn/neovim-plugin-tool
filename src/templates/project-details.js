import React from 'react'
import Layout from '../components/Layout'
import {GatsbyImage, getImage} from 'gatsby-plugin-image'
import {details, featured, htmls} from '../styles/project-details.module.css'
import { graphql } from 'gatsby'

export default function ProjectDetails({data}) {
  const { html } = data.markdownRemark
  const { title, stack, featuredImg } = data.markdownRemark.frontmatter  
  return (
    <Layout>
        <div className={details}>
            <h2>{title}</h2>
            <h3>{stack}</h3>
            <div className={featured}>
            <GatsbyImage image={getImage(featuredImg.childImageSharp.gatsbyImageData)} alt="Project Details" />
            </div>
            <div className={htmls} dangerouslySetInnerHTML={{ __html: html }} />
        </div>
    </Layout>
  )
}

export const query = graphql`
    query ProjectsDetails($slug: String) {
        markdownRemark(frontmatter: {slug: {eq: $slug}}) {
            html
            frontmatter {
                stack
                title
                featuredImg {
                    childImageSharp {
                        gatsbyImageData
                    }
                }
            }
        }
    }
`