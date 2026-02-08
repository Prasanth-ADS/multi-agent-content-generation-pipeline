import { testConnection } from './lib/huggingface-client';
import { logAgentExecution, generateRunId, printLogSummary } from './lib/logger';
import { countWords } from './lib/utils';

async function main() {
    console.log('🚀 Content Pipeline - Step 3: Logger Test\n');

    // Test Hugging Face connection
    const isConnected = await testConnection();

    if (!isConnected) {
        console.log('\n❌ Hugging Face connection failed.');
        process.exit(1);
    }

    console.log('\n✅ Hugging Face connected!\n');

    // Test logger
    console.log('📝 Testing file-based logger...\n');

    const runId = generateRunId();
    console.log(`🆔 Generated Run ID: ${runId}\n`);

    // Simulate logging an agent execution
    await logAgentExecution(
        runId,
        'test-agent',
        'This is test input for the agent',
        {
            content: 'This is test output from the agent',
            metadata: {
                agent: 'test-agent',
                timestamp: new Date(),
            },
            success: true,
        }
    );

    // Test word count utility
    const sampleText = 'This is a sample text with ten words in it.';
    const wordCount = countWords(sampleText);
    console.log(`\n🔢 Word count test: "${sampleText}"`);
    console.log(`   Result: ${wordCount} words\n`);

    // Print log summary
    printLogSummary(runId);

    console.log('✅ Logger test complete!');
    console.log('💡 Check the /logs directory for output files\n');
}

main().catch(console.error);