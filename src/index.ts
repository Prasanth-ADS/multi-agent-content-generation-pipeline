import dotenv from 'dotenv';
import logger from './lib/logger';

// Load environment variables
dotenv.config();

async function main() {
    console.log('\n');
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║                                                           ║');
    console.log('║      🚀 Content Pipeline Starting                         ║');
    console.log('║                                                           ║');
    console.log('╚═══════════════════════════════════════════════════════════╝');
    console.log('\n');

    // Confirm TypeScript is working
    const timestamp: string = new Date().toISOString();
    logger.info(`TypeScript is working! Current time: ${timestamp}`);

    // Check for OpenAI API key
    if (process.env.OPENAI_API_KEY && process.env.OPENAI_API_KEY !== 'your_openai_api_key_here') {
        logger.info('OpenAI API key detected ✓');
    } else {
        logger.warn('OpenAI API key not configured - add it to .env file');
    }

    // Display available agents
    logger.info('Available agents:', {
        agents: ['Researcher', 'Writer', 'FactChecker', 'StylePolisher']
    });

    logger.info('Pipeline ready for content generation!');
}

main().catch((error) => {
    logger.error('Pipeline failed to start', error);
    process.exit(1);
});
