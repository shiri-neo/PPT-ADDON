/**
 * PowerPoint integration using Office.js
 */

export interface SlideData {
  title: string;
  bullets: string[];
  notes?: string;
}

/**
 * Check if we're running in PowerPoint
 */
const isInPowerPoint = (): boolean => {
  return typeof PowerPoint !== 'undefined' && PowerPoint !== null;
};

/**
 * Apply multiple slides to the current PowerPoint presentation
 */
export const applySlides = async (slides: SlideData[]): Promise<void> => {
  // Check if we're running in PowerPoint
  if (!isInPowerPoint()) {
    console.log('Not running in PowerPoint - skipping slide application');
    console.log('Generated slides:', slides);
    return Promise.resolve();
  }

  return PowerPoint.run(async (context) => {
    const presentation = context.presentation;

    for (const slideData of slides) {
      // Add a new slide with Title and Content layout
      const slide = presentation.slides.add();

      // Get slide shapes
      const shapes = slide.shapes;
      shapes.load('items');
      await context.sync();

      // Add title
      const titleShape = shapes.addTextBox(slideData.title);
      titleShape.left = 50;
      titleShape.top = 40;
      titleShape.width = 600;
      titleShape.height = 60;

      const titleTextRange = titleShape.textFrame.textRange;
      titleTextRange.font.size = 32;
      titleTextRange.font.bold = true;

      // Add bullets as text box
      if (slideData.bullets.length > 0) {
        const bulletsText = slideData.bullets.map((b) => `• ${b}`).join('\n');
        const bulletShape = shapes.addTextBox(bulletsText);
        bulletShape.left = 50;
        bulletShape.top = 120;
        bulletShape.width = 600;
        bulletShape.height = 350;

        const bulletTextRange = bulletShape.textFrame.textRange;
        bulletTextRange.font.size = 18;
      }

      // Add notes if available
      if (slideData.notes) {
        slide.load('notesPage');
        await context.sync();

        // Note: Setting notes is more complex and may require additional API calls
        // For now, we'll skip this in the stub
        // TODO: Implement notes setting when needed
      }
    }

    await context.sync();
  });
};

/**
 * Update a specific slide by index
 */
export const updateSlide = async (
  slideIndex: number,
  slideData: SlideData
): Promise<void> => {
  // Check if we're running in PowerPoint
  if (!isInPowerPoint()) {
    console.log('Not running in PowerPoint - skipping slide update');
    console.log('Slide update:', { slideIndex, slideData });
    return Promise.resolve();
  }

  return PowerPoint.run(async (context) => {
    const presentation = context.presentation;
    const slides = presentation.slides;
    slides.load('items');
    await context.sync();

    if (slideIndex >= slides.items.length || slideIndex < 0) {
      throw new Error(`Slide index ${slideIndex} out of range`);
    }

    const slide = slides.items[slideIndex];
    const shapes = slide.shapes;
    shapes.load('items');
    await context.sync();

    // Clear existing text shapes (simple approach)
    // In production, you might want more sophisticated shape management
    for (let i = shapes.items.length - 1; i >= 0; i--) {
      shapes.items[i].delete();
    }
    await context.sync();

    // Add updated title
    const titleShape = shapes.addTextBox(slideData.title);
    titleShape.left = 50;
    titleShape.top = 40;
    titleShape.width = 600;
    titleShape.height = 60;

    const titleTextRange = titleShape.textFrame.textRange;
    titleTextRange.font.size = 32;
    titleTextRange.font.bold = true;

    // Add updated bullets
    if (slideData.bullets.length > 0) {
      const bulletsText = slideData.bullets.map((b) => `• ${b}`).join('\n');
      const bulletShape = shapes.addTextBox(bulletsText);
      bulletShape.left = 50;
      bulletShape.top = 120;
      bulletShape.width = 600;
      bulletShape.height = 350;

      const bulletTextRange = bulletShape.textFrame.textRange;
      bulletTextRange.font.size = 18;
    }

    await context.sync();
  });
};

/**
 * Get the current slide count
 */
export const getSlideCount = async (): Promise<number> => {
  // Check if we're running in PowerPoint
  if (!isInPowerPoint()) {
    console.log('Not running in PowerPoint - returning 0 for slide count');
    return Promise.resolve(0);
  }

  return PowerPoint.run(async (context) => {
    const slides = context.presentation.slides;
    slides.load('items');
    await context.sync();
    return slides.items.length;
  });
};
