import { PrismaClient } from '@prisma/client'
import dynamic from "next/dynamic";
import json from '../public/test-data.json'

/* 
import CourseNetwork from "../components/CourseNetwork.js"
ResizeObserver does not work with SSR - hence the fix below
https://stackoverflow.com/questions/71083857/referenceerror-resizeobserver-is-not-defined-with-nivo-and-nextjs
*/
const CourseNetwork = dynamic(() => import("../components/CourseNetwork.js"), {
  ssr: false
})

export async function getStaticProps() {
  const prisma = new PrismaClient()
  const courses = await prisma.eecs.findMany()

  return {
    props: {
      courses
    }
  }
}

export default ({ courses }) => (
  <>
    <div style={{ height: "400px" }}>
      <CourseNetwork data={json}/>
    </div>
    <ul>
    {courses.map((course) => (
      <li>{course.course_code}</li>
    ))}
  </ul>
  </>
);