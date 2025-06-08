import { defineCollection, z } from 'astro:content';

const digestCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string()
      .min(1, "Title cannot be empty")
      .max(200, "Title is too long"),
    pubDate: z.string()
      .regex(/^\d{4}-\d{2}-\d{2}$/, "Date must be in YYYY-MM-DD format"),
    description: z.string()
      .min(1, "Description cannot be empty")
      .max(500, "Description is too long"),
  }),
});

export const collections = {
  'digests': digestCollection,
}; 