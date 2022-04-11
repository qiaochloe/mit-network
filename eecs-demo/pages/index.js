import { PrismaClient } from '@prisma/client'

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
  <ul>
    {courses.map((course) => (
      <li>{course.course_code}</li>
    ))}
  </ul>
);