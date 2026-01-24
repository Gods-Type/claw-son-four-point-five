/**
 * Main page component for claw-son-four-point-five education platform.
 * 
 * This page serves as the entry point for the educational platform,
 * providing an overview of available learning paths and features.
 */

import { GetStaticProps } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  BookOpen, 
  Brain, 
  Target, 
  Users, 
  Code2, 
  Award,
  TrendingUp,
  CheckCircle2,
  Play,
  ArrowRight
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';

// Mock data - in real implementation, this would come from API
const learningPaths = [
  {
    id: 'foundational',
    title: 'Foundational Path',
    description: 'Learn AI fundamentals and basic limitations',
    difficulty: 'Beginner',
    duration: '4-6 weeks',
    icon: BookOpen,
    color: 'bg-green-500',
    modules: [
      { title: 'AI Fundamentals', completed: true },
      { title: 'Understanding Limitations', completed: true },
      { title: 'Ethical Considerations', completed: false },
      { title: 'Basic Hands-on Examples', completed: false },
    ],
    progress: 50,
  },
  {
    id: 'technical',
    title: 'Technical Path',
    description: 'Deep dive into technical limitations and solutions',
    difficulty: 'Intermediate',
    duration: '8-10 weeks',
    icon: Code2,
    color: 'bg-blue-500',
    modules: [
      { title: 'Technical Limitations Overview', completed: true },
      { title: 'Common Sense & Reasoning', completed: false },
      { title: 'Explainability Methods', completed: false },
      { title: 'Implementation Projects', completed: false },
      { title: 'Case Study Analysis', completed: false },
    ],
    progress: 20,
  },
  {
    id: 'advanced',
    title: 'Advanced Path',
    description: 'Advanced solutions and research contributions',
    difficulty: 'Advanced',
    duration: '12-16 weeks',
    icon: Brain,
    color: 'bg-purple-500',
    modules: [
      { title: 'Advanced Solution Approaches', completed: false },
      { title: 'Neuro-Symbolic Integration', completed: false },
      { title: 'Implementation Projects', completed: false },
      { title: 'Research Methodology', completed: false },
      { title: 'Critical Analysis', completed: false },
      { title: 'Research Contributions', completed: false },
    ],
    progress: 0,
  },
];

const recentActivity = [
  { id: 1, type: 'tutorial', title: 'Completed: AI Fundamentals', time: '2 hours ago' },
  { id: 2, type: 'exercise', title: 'Submitted: Bias Detection Exercise', time: '5 hours ago' },
  { id: 3, type: 'quiz', title: 'Scored 85% on Technical Limitations Quiz', time: '1 day ago' },
  { id: 4, type: 'certificate', title: 'Earned: AI Ethics Basics Certificate', time: '2 days ago' },
];

const stats = [
  { label: 'Tutorials Completed', value: '12', icon: CheckCircle2 },
  { label: 'Exercises Solved', value: '48', icon: Target },
  { label: 'Learning Hours', value: '156', icon: BookOpen },
  { label: 'Achievement Points', value: '2,450', icon: Award },
];

interface HomePageProps {
  initialData?: {
    userProgress?: any;
    recentActivity?: any[];
  };
}

export default function HomePage({ initialData }: HomePageProps) {
  const [selectedPath, setSelectedPath] = useState(learningPaths[0]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null; // Prevent hydration issues
  }

  return (
    <>
      <Head>
        <title>Claw Son Four Point Five - AI Education Platform</title>
        <meta
          name="description"
          content="Learn about AI limitations and solutions through interactive tutorials, hands-on exercises, and comprehensive assessments."
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <div className="absolute inset-0 bg-black opacity-20" />
          <div className="relative container mx-auto px-4 py-24 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="max-w-4xl mx-auto text-center"
            >
              <Badge variant="secondary" className="mb-4 text-purple-100 bg-purple-800">
                🎓 Educational Platform
              </Badge>
              <h1 className="text-4xl md:text-6xl font-bold mb-6">
                Understanding AI Limitations
                <span className="block text-yellow-300">Building Solutions</span>
              </h1>
              <p className="text-xl md:text-2xl mb-8 text-blue-100">
                Master the challenges facing modern AI and learn cutting-edge approaches to overcome them through interactive learning.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg" variant="secondary" className="bg-white text-blue-600 hover:bg-blue-50">
                  <Play className="mr-2 h-4 w-4" />
                  Start Learning
                </Button>
                <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
                  Explore Paths
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </motion.div>
          </div>
          
          {/* Animated background elements */}
          <motion.div
            className="absolute top-20 left-10 w-20 h-20 bg-yellow-300 rounded-full opacity-20"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.2, 0.3, 0.2],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <motion.div
            className="absolute bottom-20 right-10 w-32 h-32 bg-purple-300 rounded-full opacity-20"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.2, 0.4, 0.2],
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 1
            }}
          />
        </section>

        {/* Stats Section */}
        <section className="py-12 bg-white shadow-sm">
          <div className="container mx-auto px-4 lg:px-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="flex justify-center mb-2">
                    <stat.icon className="h-8 w-8 text-blue-600" />
                  </div>
                  <div className="text-3xl font-bold text-gray-900">{stat.value}</div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Learning Paths Section */}
        <section className="py-16">
          <div className="container mx-auto px-4 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Choose Your Learning Path
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Select a path that matches your current level and goals. Each path builds comprehensive understanding through structured progression.
              </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-8 mb-12">
              {learningPaths.map((path, index) => (
                <motion.div
                  key={path.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Card 
                    className={`h-full cursor-pointer transition-all duration-300 hover:shadow-xl ${
                      selectedPath.id === path.id ? 'ring-2 ring-blue-500 shadow-lg' : ''
                    }`}
                    onClick={() => setSelectedPath(path)}
                  >
                    <CardHeader>
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded-lg ${path.color}`}>
                          <path.icon className="h-6 w-6 text-white" />
                        </div>
                        <div>
                          <CardTitle className="text-lg">{path.title}</CardTitle>
                          <Badge variant="outline">{path.difficulty}</Badge>
                        </div>
                      </div>
                      <CardDescription>{path.description}</CardDescription>
                      <div className="text-sm text-gray-500">
                        <span className="flex items-center">
                          <BookOpen className="h-4 w-4 mr-1" />
                          {path.duration}
                        </span>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium">Progress</span>
                          <span className="text-sm text-gray-500">{path.progress}%</span>
                        </div>
                        <Progress value={path.progress} className="h-2" />
                        <div className="space-y-1 mt-4">
                          {path.modules.slice(0, 3).map((module, idx) => (
                            <div key={idx} className="flex items-center space-x-2 text-sm">
                              {module.completed ? (
                                <CheckCircle2 className="h-4 w-4 text-green-500" />
                              ) : (
                                <div className="h-4 w-4 border border-gray-300 rounded-full" />
                              )}
                              <span className={module.completed ? 'text-green-700' : 'text-gray-600'}>
                                {module.title}
                              </span>
                            </div>
                          ))}
                          {path.modules.length > 3 && (
                            <div className="text-sm text-gray-500">
                              +{path.modules.length - 3} more modules
                            </div>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>

            <div className="text-center">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                Continue with {selectedPath.title}
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Learning Features
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Our platform provides comprehensive tools and features to enhance your learning experience.
              </p>
            </motion.div>

            <Tabs defaultValue="interactive" className="max-w-4xl mx-auto">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="interactive">Interactive</TabsTrigger>
                <TabsTrigger value="assessment">Assessment</TabsTrigger>
                <TabsTrigger value="collaboration">Collaboration</TabsTrigger>
                <TabsTrigger value="analytics">Analytics</TabsTrigger>
              </TabsList>
              
              <TabsContent value="interactive" className="mt-8">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Code2 className="mr-2 h-5 w-5" />
                      Interactive Learning
                    </CardTitle>
                    <CardDescription>
                      Hands-on experience with live code editors and real-time feedback.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-2">Live Code Editor</h4>
                        <p className="text-gray-600">Write and execute code directly in your browser with Monaco Editor.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Visualizations</h4>
                        <p className="text-gray-600">Interactive plots and diagrams to understand complex concepts.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Step-by-Step Guidance</h4>
                        <p className="text-gray-600">Detailed instructions with hints and solutions.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Real Examples</h4>
                        <p className="text-gray-600">Real-world case studies and practical applications.</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="assessment" className="mt-8">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Target className="mr-2 h-5 w-5" />
                      Comprehensive Assessment
                    </CardTitle>
                    <CardDescription>
                      Track your progress with automated grading and detailed feedback.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-2">Automated Grading</h4>
                        <p className="text-gray-600">Instant feedback on coding exercises and quizzes.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Peer Review</h4>
                        <p className="text-gray-600">Learn from others through collaborative review.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Progress Tracking</h4>
                        <p className="text-gray-600">Monitor your learning journey with detailed analytics.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Achievements</h4>
                        <p className="text-gray-600">Earn certificates and badges for milestones.</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="collaboration" className="mt-8">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Users className="mr-2 h-5 w-5" />
                      Collaborative Learning
                    </CardTitle>
                    <CardDescription>
                      Connect with peers and experts for enhanced learning.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-2">Discussion Forums</h4>
                        <p className="text-gray-600">Engage in topic-based discussions with the community.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Study Groups</h4>
                        <p className="text-gray-600">Form groups for collaborative learning and support.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Expert Mentorship</h4>
                        <p className="text-gray-600">Get guidance from AI experts and researchers.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Knowledge Sharing</h4>
                        <p className="text-gray-600">Contribute your own content and insights.</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="analytics" className="mt-8">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <TrendingUp className="mr-2 h-5 w-5" />
                      Learning Analytics
                    </CardTitle>
                    <CardDescription>
                      Detailed insights into your learning patterns and progress.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-2">Performance Metrics</h4>
                        <p className="text-gray-600">Track quiz scores, completion rates, and learning velocity.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Personalized Recommendations</h4>
                        <p className="text-gray-600">AI-powered suggestions for next learning steps.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Time Analytics</h4>
                        <p className="text-gray-600">Understand how you spend your learning time.</p>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Skill Progression</h4>
                        <p className="text-gray-600">Visualize your skill development over time.</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </section>

        {/* Recent Activity Section */}
        <section className="py-16 bg-white">
          <div className="container mx-auto px-4 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Recent Activity
              </h2>
              <p className="text-xl text-gray-600">
                Your latest learning activities and achievements.
              </p>
            </motion.div>

            <div className="max-w-2xl mx-auto">
              <Card>
                <CardHeader>
                  <CardTitle>Learning Timeline</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentActivity.map((activity, index) => (
                      <div key={activity.id} className="flex items-center justify-between py-3 border-b last:border-b-0">
                        <div className="flex items-center space-x-3">
                          <div className="p-2 bg-blue-100 rounded-full">
                            <CheckCircle2 className="h-4 w-4 text-blue-600" />
                          </div>
                          <div>
                            <p className="font-medium">{activity.title}</p>
                            <p className="text-sm text-gray-500">{activity.time}</p>
                          </div>
                        </div>
                        <Badge variant="outline" className="capitalize">
                          {activity.type}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}

export const getStaticProps: GetStaticProps = async () => {
  // In a real implementation, this would fetch data from your API
  // For now, we'll return mock data
  return {
    props: {
      initialData: {
        userProgress: {
          completedTutorials: 12,
          currentPath: 'technical',
          totalHours: 156,
        },
        recentActivity: recentActivity,
      },
    },
    revalidate: 60, // Revalidate every minute
  };
};