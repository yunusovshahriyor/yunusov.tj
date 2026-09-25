import { Hero } from "@/components/sections/Hero";
import { About } from "@/components/sections/About";
import { Projects } from "@/components/sections/Projects";
import { Services } from "@/components/sections/Services";
import { Process } from "@/components/sections/Process";
import { Technologies } from "@/components/sections/Technologies";
import { Blog } from "@/components/sections/Blog";
import { Courses } from "@/components/sections/Courses";
import { Contact } from "@/components/sections/Contact";

export default function Home() {
  return (
    <>
      <Hero />
      <About />
      <Projects />
      <Services />
      <Process />
      <Technologies />
      <Blog />
      <Courses />
      <Contact />
    </>
  );
}
